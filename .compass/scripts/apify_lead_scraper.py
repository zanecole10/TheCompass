"""
Apify Lead Scraper Script
=========================
Scrapes Google Maps for companies in specified niches using Apify's Google Maps Scraper.

Usage:
    python apify_lead_scraper.py

Workflow:
    1. Start Google Maps Scraper actor run
    2. Poll until complete (with timeout)
    3. Retrieve and process results
    4. Save to user-workspace/{niche-slug}-leads.json
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

APIFY_API_KEY = ""  # Set via environment variable or pass to functions
BASE_URL = "https://api.apify.com/v2"

# Google Maps Scraper Actor ID
ACTOR_ID = "nwua9Gu5YrADL7ZDj"

# Pricing: $0.004 per place
COST_PER_PLACE = 0.004

# Timeouts
MAX_WAIT_SECONDS = 600  # 10 minutes max wait
POLL_INTERVAL = 10  # Check every 10 seconds

# =============================================================================
# API CLIENT
# =============================================================================

class ApifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make API request to Apify."""
        url = f"{BASE_URL}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json() if response.text else {}

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise

    # =========================================================================
    # ACTOR ENDPOINTS
    # =========================================================================

    def start_scraper(
        self,
        search_query: str,
        max_places: int = 600,
        language: str = "en"
    ) -> dict:
        """
        Start Google Maps Scraper actor run.

        Args:
            search_query: e.g., "HVAC companies in California"
            max_places: Maximum places to scrape (default 600)
            language: Language for results (default "en")

        Returns:
            Run info including run ID
        """
        payload = {
            "searchStringsArray": [search_query],
            "maxCrawledPlacesPerSearch": max_places,
            "language": language,
            "includeWebsites": True,
            "includeEmails": True,
            "includePhones": True,
            "skipClosedPlaces": False,
            "scrapeDirectories": False,
            "deeperCityScrape": False,
            "oneReviewPerRow": False,
            "allPlacesNoSearch": False
        }

        print(f"Starting Google Maps scraper: {search_query}")
        print(f"Max places: {max_places}")

        result = self._request("POST", f"/acts/{ACTOR_ID}/runs", payload)
        run_id = result.get("data", {}).get("id")
        print(f"Run started: {run_id}")
        return result

    def get_run_status(self, run_id: str) -> dict:
        """Get status of an actor run."""
        result = self._request("GET", f"/actor-runs/{run_id}")
        return result.get("data", {})

    def wait_for_completion(self, run_id: str, timeout: int = MAX_WAIT_SECONDS) -> dict:
        """
        Poll until run completes or times out.

        Returns:
            Final run status
        """
        start_time = time.time()
        last_status = None

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Scraper timed out after {timeout} seconds")

            status_data = self.get_run_status(run_id)
            status = status_data.get("status")

            if status != last_status:
                print(f"Status: {status} ({int(elapsed)}s elapsed)")
                last_status = status

            if status == "SUCCEEDED":
                print("Scraper completed successfully!")
                return status_data

            if status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                raise Exception(f"Scraper {status}: {status_data.get('statusMessage', 'Unknown error')}")

            time.sleep(POLL_INTERVAL)

    def get_dataset_items(self, dataset_id: str) -> List[dict]:
        """
        Retrieve all items from a dataset.

        Returns:
            List of scraped places
        """
        print(f"Retrieving results from dataset: {dataset_id}")

        # Get items with pagination
        all_items = []
        offset = 0
        limit = 1000

        while True:
            response = requests.get(
                f"{BASE_URL}/datasets/{dataset_id}/items",
                headers=self.headers,
                params={"offset": offset, "limit": limit, "format": "json"}
            )
            response.raise_for_status()
            items = response.json()

            if not items:
                break

            all_items.extend(items)
            print(f"Retrieved {len(all_items)} items...")

            if len(items) < limit:
                break

            offset += limit

        print(f"Total items retrieved: {len(all_items)}")
        return all_items


# =============================================================================
# DATA PROCESSING
# =============================================================================

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def extract_domain(website: str) -> Optional[str]:
    """Extract domain from website URL."""
    if not website:
        return None

    # Remove protocol
    domain = re.sub(r'^https?://', '', website)
    # Remove www.
    domain = re.sub(r'^www\.', '', domain)
    # Remove path
    domain = domain.split('/')[0]
    # Remove port
    domain = domain.split(':')[0]

    return domain if domain else None


def process_leads(raw_places: List[dict], niche: str, location: str) -> dict:
    """
    Process raw Apify results into clean lead data.

    Returns:
        Processed leads data structure
    """
    print(f"Processing {len(raw_places)} places...")

    leads = []
    seen_domains = set()
    emails_found = 0

    for place in raw_places:
        # Extract basic info
        company_name = place.get("title", "").strip()
        if not company_name:
            continue

        website = place.get("website", "")
        domain = extract_domain(website)

        # Skip duplicates based on domain
        if domain and domain in seen_domains:
            continue
        if domain:
            seen_domains.add(domain)

        # Extract email (if available from Google Maps)
        email = place.get("email", "")
        if email:
            emails_found += 1

        # Build lead record
        lead = {
            "company_name": company_name,
            "location": place.get("city", "") or place.get("state", "") or location,
            "address": place.get("address", ""),
            "phone": place.get("phone", ""),
            "website": website,
            "domain": domain,
            "email": email,
            "rating": place.get("totalScore"),
            "review_count": place.get("reviewsCount", 0),
            "categories": place.get("categories", []),
            "hours": place.get("openingHours", ""),
            "place_id": place.get("placeId", ""),
            "google_maps_url": place.get("url", "")
        }

        leads.append(lead)

    # Calculate stats
    total_found = len(leads)
    find_rate = (emails_found / total_found * 100) if total_found > 0 else 0
    estimated_cost = len(raw_places) * COST_PER_PLACE

    result = {
        "niche": niche,
        "location": location,
        "total_found": total_found,
        "emails_found": emails_found,
        "find_rate": f"{find_rate:.1f}%",
        "estimated_cost": f"${estimated_cost:.2f}",
        "scraped_at": datetime.now().isoformat(),
        "leads": leads
    }

    print(f"Processed {total_found} unique companies")
    print(f"Emails found: {emails_found} ({find_rate:.1f}%)")
    print(f"Estimated cost: ${estimated_cost:.2f}")

    return result


# =============================================================================
# MAIN SCRAPER FUNCTION
# =============================================================================

def scrape_leads(
    client: ApifyClient,
    niche: str,
    location: str,
    max_places: int = 600,
    output_dir: str = "user-workspace"
) -> dict:
    """
    Complete lead scraping workflow for a niche.

    Args:
        client: ApifyClient instance
        niche: e.g., "HVAC inspection companies"
        location: e.g., "California"
        max_places: Maximum places to scrape
        output_dir: Directory to save results

    Returns:
        Processed leads data
    """
    print(f"\n{'='*60}")
    print(f"Scraping: {niche} in {location}")
    print(f"{'='*60}")

    # Build search query
    search_query = f"{niche} in {location}"

    # Step 1: Start scraper
    run_result = client.start_scraper(search_query, max_places)
    run_data = run_result.get("data", {})
    run_id = run_data.get("id")
    dataset_id = run_data.get("defaultDatasetId")

    if not run_id:
        raise Exception("Failed to start scraper - no run ID returned")

    print(f"Run ID: {run_id}")
    print(f"Dataset ID: {dataset_id}")

    # Step 2: Wait for completion
    final_status = client.wait_for_completion(run_id)

    # Step 3: Retrieve results
    raw_places = client.get_dataset_items(dataset_id)

    if not raw_places:
        print("WARNING: No places found!")
        return {
            "niche": niche,
            "location": location,
            "total_found": 0,
            "emails_found": 0,
            "find_rate": "0%",
            "estimated_cost": "$0.00",
            "scraped_at": datetime.now().isoformat(),
            "leads": [],
            "apify_run_id": run_id
        }

    # Step 4: Process results
    processed = process_leads(raw_places, niche, location)
    processed["apify_run_id"] = run_id

    # Step 5: Save to file
    niche_slug = slugify(niche)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{niche_slug}-leads.json")

    with open(output_file, "w") as f:
        json.dump(processed, f, indent=2)

    print(f"\n✅ SCRAPING COMPLETE: {niche}")
    print(f"   Companies found: {processed['total_found']}")
    print(f"   Emails found: {processed['emails_found']} ({processed['find_rate']})")
    print(f"   Cost: {processed['estimated_cost']}")
    print(f"   Saved to: {output_file}")

    return processed


def scrape_multiple_niches(
    client: ApifyClient,
    niches: List[dict],
    output_dir: str = "user-workspace"
) -> List[dict]:
    """
    Scrape leads for multiple niches.

    Args:
        client: ApifyClient instance
        niches: List of {"niche": "...", "location": "...", "max_places": 600}
        output_dir: Directory to save results

    Returns:
        List of processed lead data for each niche
    """
    results = []

    for i, niche_config in enumerate(niches, 1):
        print(f"\n[{i}/{len(niches)}] Processing niche...")

        try:
            result = scrape_leads(
                client=client,
                niche=niche_config["niche"],
                location=niche_config.get("location", "United States"),
                max_places=niche_config.get("max_places", 600),
                output_dir=output_dir
            )
            results.append(result)

        except Exception as e:
            print(f"ERROR scraping {niche_config['niche']}: {e}")
            results.append({
                "niche": niche_config["niche"],
                "error": str(e)
            })

        # Small delay between niches
        if i < len(niches):
            print("Waiting 5 seconds before next niche...")
            time.sleep(5)

    # Summary
    print(f"\n{'='*60}")
    print("SCRAPING SUMMARY")
    print(f"{'='*60}")

    total_leads = 0
    total_emails = 0
    total_cost = 0

    for r in results:
        if "error" not in r:
            print(f"✅ {r['niche']}: {r['total_found']} companies, {r['emails_found']} emails")
            total_leads += r['total_found']
            total_emails += r['emails_found']
            total_cost += float(r['estimated_cost'].replace('$', ''))
        else:
            print(f"❌ {r['niche']}: {r['error']}")

    print(f"\nTotal: {total_leads} companies, {total_emails} emails")
    print(f"Total cost: ${total_cost:.2f}")

    return results


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("""
    Apify Lead Scraper
    ==================

    This script scrapes Google Maps for companies using Apify's scraper.

    Usage:

        from apify_lead_scraper import ApifyClient, scrape_leads, scrape_multiple_niches

        # Initialize client
        client = ApifyClient("your_apify_api_key")

        # Single niche
        result = scrape_leads(
            client=client,
            niche="HVAC inspection companies",
            location="California",
            max_places=600
        )

        # Multiple niches (Mission 2)
        niches = [
            {"niche": "HVAC inspection companies", "location": "California", "max_places": 600},
            {"niche": "Fire inspection companies", "location": "California", "max_places": 600},
            {"niche": "Property management companies", "location": "California", "max_places": 600}
        ]
        results = scrape_multiple_niches(client, niches)

    Output saved to: user-workspace/{niche-slug}-leads.json

    Cost: ~$2.40 per niche (600 places × $0.004)
    Time: ~2-5 minutes per niche
    """)
