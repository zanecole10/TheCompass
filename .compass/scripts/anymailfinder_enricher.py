"""
AnyMailFinder Enricher Script
=============================
Finds decision-maker emails for companies using AnyMailFinder API.

Key Features:
- Saves progress incrementally (won't lose work if interrupted)
- Can resume from where it left off
- Handles rate limiting (1 request/second)
- Shows clear progress updates
- Robust error handling

Usage:
    python anymailfinder_enricher.py

Workflow:
    1. Load leads from {niche}-leads.json
    2. For each lead with a domain, call AnyMailFinder API
    3. Save progress after EVERY successful lookup
    4. Output enriched leads to {niche}-enriched.json
"""

import requests
import json
import time
import re
import os
from datetime import datetime
from typing import List, Dict, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

ANYMAILFINDER_API_KEY = ""  # Set via environment variable or pass to functions
BASE_URL = "https://api.anymailfinder.com/v5.0/search/decision-maker.json"

# Rate limiting: AnyMailFinder allows ~1 request/second
REQUEST_DELAY = 1.0  # seconds between requests

# Save progress every N leads (in addition to saving after each successful find)
SAVE_INTERVAL = 10

# =============================================================================
# API CLIENT
# =============================================================================

class AnyMailFinderClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.requests_made = 0
        self.emails_found = 0
        self.errors = 0

    def find_decision_maker(self, domain: str, category: str = "ceo") -> Optional[dict]:
        """
        Find decision-maker email for a domain.

        Args:
            domain: Company domain (e.g., "acmehvac.com")
            category: Decision maker type - "ceo", "cfo", "cto", etc.

        Returns:
            Dict with email, name, title if found, None otherwise
        """
        payload = {
            "domain": domain,
            "decision_maker_category": category
        }

        try:
            response = requests.post(
                BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            self.requests_made += 1

            if response.status_code == 200:
                data = response.json()

                # Check if email was found
                email = data.get("email")
                if email and "@" in email:
                    self.emails_found += 1
                    return {
                        "email": email,
                        "full_name": data.get("personFullName", ""),
                        "first_name": self._extract_first_name(data.get("personFullName", "")),
                        "last_name": self._extract_last_name(data.get("personFullName", "")),
                        "title": data.get("personJobTitle", ""),
                        "linkedin_url": data.get("personLinkedinUrl", ""),
                        "confidence": data.get("confidence", ""),
                        "verification": data.get("verification", "")
                    }
                return None

            elif response.status_code == 401:
                print(f"ERROR: Invalid API key")
                self.errors += 1
                return None

            elif response.status_code == 402:
                print(f"ERROR: Out of credits")
                self.errors += 1
                return None

            elif response.status_code == 429:
                print(f"Rate limited - waiting 5 seconds...")
                time.sleep(5)
                return self.find_decision_maker(domain, category)  # Retry

            else:
                self.errors += 1
                return None

        except requests.exceptions.Timeout:
            print(f"Timeout for {domain}")
            self.errors += 1
            return None

        except Exception as e:
            print(f"Error for {domain}: {e}")
            self.errors += 1
            return None

    def _extract_first_name(self, full_name: str) -> str:
        """Extract first name from full name."""
        if not full_name:
            return ""
        parts = full_name.strip().split()
        return parts[0] if parts else ""

    def _extract_last_name(self, full_name: str) -> str:
        """Extract last name from full name."""
        if not full_name:
            return ""
        parts = full_name.strip().split()
        return parts[-1] if len(parts) > 1 else ""


# =============================================================================
# DOMAIN EXTRACTION
# =============================================================================

def extract_domain(website: str) -> Optional[str]:
    """Extract clean domain from website URL."""
    if not website:
        return None

    # Remove protocol
    domain = re.sub(r'^https?://', '', website)
    # Remove www.
    domain = re.sub(r'^www\.', '', domain)
    # Remove path and query
    domain = domain.split('/')[0].split('?')[0]
    # Remove port
    domain = domain.split(':')[0]

    # Validate domain has at least one dot
    if '.' not in domain:
        return None

    return domain.lower() if domain else None


# =============================================================================
# PROGRESS TRACKING
# =============================================================================

def load_progress(progress_file: str) -> dict:
    """Load progress from checkpoint file."""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"processed_domains": {}, "last_index": 0}


def save_progress(progress_file: str, progress: dict):
    """Save progress to checkpoint file."""
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


# =============================================================================
# MAIN ENRICHMENT FUNCTION
# =============================================================================

def enrich_leads(
    client: AnyMailFinderClient,
    input_file: str,
    output_file: str,
    progress_file: str = None
) -> dict:
    """
    Enrich leads with decision-maker emails.

    Args:
        client: AnyMailFinderClient instance
        input_file: Path to leads JSON file (from Apify scraper)
        output_file: Path to save enriched leads
        progress_file: Path to checkpoint file (auto-generated if None)

    Returns:
        Enrichment stats
    """
    # Load input leads
    print(f"Loading leads from: {input_file}")
    with open(input_file, 'r') as f:
        data = json.load(f)

    leads = data.get("leads", [])
    total_leads = len(leads)
    print(f"Total leads to process: {total_leads}")

    # Set up progress file
    if progress_file is None:
        progress_file = input_file.replace(".json", "-progress.json")

    # Load existing progress
    progress = load_progress(progress_file)
    processed_domains = progress.get("processed_domains", {})
    start_index = progress.get("last_index", 0)

    print(f"Resuming from index: {start_index}")
    print(f"Previously processed: {len(processed_domains)} domains")
    print(f"Previously found: {sum(1 for v in processed_domains.values() if v.get('email'))} emails")
    print()

    # Process each lead
    enriched_leads = []
    emails_found = 0
    domains_processed = 0

    for i, lead in enumerate(leads):
        # Get domain
        domain = lead.get("domain") or extract_domain(lead.get("website", ""))

        if not domain:
            # No domain - keep lead as-is
            enriched_leads.append(lead)
            continue

        # Check if already processed
        if domain in processed_domains:
            # Use cached result
            cached = processed_domains[domain]
            if cached.get("email"):
                lead["email"] = cached["email"]
                lead["first_name"] = cached.get("first_name", "")
                lead["last_name"] = cached.get("last_name", "")
                lead["decision_maker_title"] = cached.get("title", "")
                emails_found += 1
            enriched_leads.append(lead)
            continue

        # Skip if before resume point
        if i < start_index:
            enriched_leads.append(lead)
            continue

        # Call AnyMailFinder API
        domains_processed += 1
        result = client.find_decision_maker(domain)

        # Store result (even if None, to avoid re-processing)
        processed_domains[domain] = result or {"email": None}

        if result:
            lead["email"] = result["email"]
            lead["first_name"] = result["first_name"]
            lead["last_name"] = result["last_name"]
            lead["decision_maker_title"] = result["title"]
            lead["linkedin_url"] = result.get("linkedin_url", "")
            emails_found += 1

            # Save progress immediately after finding an email
            progress["processed_domains"] = processed_domains
            progress["last_index"] = i + 1
            save_progress(progress_file, progress)

        enriched_leads.append(lead)

        # Progress update every 10 leads
        if domains_processed % 10 == 0:
            print(f"Progress: {i+1}/{total_leads} | Domains checked: {domains_processed} | Emails found: {emails_found} | Rate: {emails_found/max(domains_processed,1)*100:.1f}%")

            # Save progress periodically
            progress["processed_domains"] = processed_domains
            progress["last_index"] = i + 1
            save_progress(progress_file, progress)

        # Rate limiting
        time.sleep(REQUEST_DELAY)

    # Final save
    print()
    print(f"Enrichment complete!")
    print(f"Total leads: {total_leads}")
    print(f"Domains processed this run: {domains_processed}")
    print(f"Total emails found: {emails_found}")
    print(f"Find rate: {emails_found/max(domains_processed,1)*100:.1f}%")

    # Build output data
    output_data = {
        "niche": data.get("niche", ""),
        "location": data.get("location", ""),
        "total_leads": len(enriched_leads),
        "emails_found": emails_found,
        "find_rate": f"{emails_found/max(len(enriched_leads),1)*100:.1f}%",
        "enriched_at": datetime.now().isoformat(),
        "source_file": input_file,
        "leads": enriched_leads,
        "enrichment_stats": {
            "api_requests": client.requests_made,
            "emails_found": client.emails_found,
            "errors": client.errors
        }
    }

    # Save enriched leads
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved to: {output_file}")

    # Clean up progress file on successful completion
    if os.path.exists(progress_file):
        os.remove(progress_file)
        print(f"Cleaned up progress file")

    return output_data


def enrich_multiple_niches(
    client: AnyMailFinderClient,
    input_files: List[str],
    output_dir: str = None
) -> List[dict]:
    """
    Enrich leads for multiple niches.

    Args:
        client: AnyMailFinderClient instance
        input_files: List of paths to leads JSON files
        output_dir: Directory for output files (defaults to same as input)

    Returns:
        List of enrichment results
    """
    results = []

    for i, input_file in enumerate(input_files, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(input_files)}] Enriching: {input_file}")
        print(f"{'='*60}")

        # Determine output file
        if output_dir:
            filename = os.path.basename(input_file).replace("-leads.json", "-enriched.json")
            output_file = os.path.join(output_dir, filename)
        else:
            output_file = input_file.replace("-leads.json", "-enriched.json")

        try:
            result = enrich_leads(client, input_file, output_file)
            results.append(result)
        except Exception as e:
            print(f"ERROR enriching {input_file}: {e}")
            results.append({"error": str(e), "file": input_file})

    # Summary
    print(f"\n{'='*60}")
    print("ENRICHMENT SUMMARY")
    print(f"{'='*60}")

    total_emails = 0
    for r in results:
        if "error" not in r:
            print(f"✅ {r.get('niche', 'Unknown')}: {r['emails_found']} emails ({r['find_rate']})")
            total_emails += r['emails_found']
        else:
            print(f"❌ {r['file']}: {r['error']}")

    print(f"\nTotal emails found: {total_emails}")

    return results


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("""
    AnyMailFinder Enricher
    ======================

    This script finds decision-maker emails for your scraped leads.

    Features:
    - Saves progress after EVERY email found (won't lose work if interrupted)
    - Can resume from where it left off
    - Handles rate limiting automatically
    - Shows clear progress updates

    Usage:

        from anymailfinder_enricher import AnyMailFinderClient, enrich_leads, enrich_multiple_niches

        # Initialize client
        client = AnyMailFinderClient("your_anymailfinder_api_key")

        # Single file
        result = enrich_leads(
            client=client,
            input_file="user-workspace/hvac-leads.json",
            output_file="user-workspace/hvac-enriched.json"
        )

        # Multiple files (Mission 2)
        input_files = [
            "user-workspace/hvac-leads.json",
            "user-workspace/fire-inspection-leads.json",
            "user-workspace/property-management-leads.json"
        ]
        results = enrich_multiple_niches(client, input_files)

    Output: {niche}-enriched.json with decision-maker emails

    Expected find rate: 50-60%
    Time: ~1 second per lead (API rate limit)
    For 600 leads: ~10-15 minutes per niche
    """)
