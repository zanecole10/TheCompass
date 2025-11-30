"""
Instantly Campaign Launcher Script
===================================
Creates campaigns with embedded sequences, uploads leads, and activates campaigns.

Usage:
    python instantly_campaign_launcher.py

Workflow:
    1. Create campaign with embedded 3-step sequence (Day 0, Day 3, Day 7)
    2. Add leads in bulk with custom variables
    3. Activate campaign
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

INSTANTLY_API_KEY = ""  # Set via environment variable or config file
BASE_URL = "https://api.instantly.ai/api/v2"

# =============================================================================
# API CLIENT
# =============================================================================

class InstantlyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make API request to Instantly."""
        url = f"{BASE_URL}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
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
    # CAMPAIGN ENDPOINTS
    # =========================================================================

    def create_campaign(
        self,
        name: str,
        from_emails: List[str],
        daily_limit: int = 25
    ) -> dict:
        """
        Step 1: Create campaign with embedded 3-step email sequence.

        Endpoint: POST /api/v2/campaigns

        Sequences are embedded in the campaign creation - NOT created separately.
        The sequences array uses custom variables that are populated per-lead.

        Delays are RELATIVE to previous step:
        - Email 1: delay 0 (Day 0)
        - Email 2: delay 3 (3 days after Email 1 = Day 3)
        - Email 3: delay 4 (4 days after Email 2 = Day 7)
        """
        payload = {
            "name": name,
            "campaign_schedule": {
                "schedules": [
                    {
                        "name": f"{name} Schedule",
                        "timing": {
                            "from": "09:00",
                            "to": "17:00"
                        },
                        "days": {
                            "monday": True,
                            "tuesday": True,
                            "wednesday": True,
                            "thursday": True,
                            "friday": True,
                            "saturday": False,
                            "sunday": False
                        },
                        "timezone": "America/Los_Angeles"  # Pacific Time
                    }
                ]
            },
            "sequences": [
                {
                    "steps": [
                        # Email 1 - Day 0 (Initial email with A/B/C subject testing)
                        {
                            "type": "email",
                            "delay": 0,
                            "variants": [
                                {
                                    "subject": "{{subject_variant_a}}",
                                    "body": "{{email_body}}"
                                },
                                {
                                    "subject": "{{subject_variant_b}}",
                                    "body": "{{email_body}}"
                                },
                                {
                                    "subject": "{{subject_variant_c}}",
                                    "body": "{{email_body}}"
                                }
                            ]
                        },
                        # Email 2 - Day 3 (Follow-up)
                        {
                            "type": "email",
                            "delay": 3,
                            "variants": [
                                {
                                    "subject": "Re: {{subject_variant_a}}",
                                    "body": "{{follow_up_day_3}}"
                                }
                            ]
                        },
                        # Email 3 - Day 7 (Final follow-up)
                        # delay: 4 = 4 days after Email 2 = Day 7 total
                        {
                            "type": "email",
                            "delay": 4,
                            "variants": [
                                {
                                    "subject": "Last note - {{problemAngle}}",
                                    "body": "{{follow_up_day_7}}"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        print(f"Creating campaign: {name}")
        result = self._request("POST", "/campaigns", payload)
        print(f"Campaign created: {result.get('id')}")
        return result

    def activate_campaign(self, campaign_id: str) -> dict:
        """
        Step 3: Activate campaign to start sending.

        Endpoint: POST /api/v2/campaigns/{campaign_id}/activate
        """
        print(f"Activating campaign: {campaign_id}")
        result = self._request("POST", f"/campaigns/{campaign_id}/activate")
        print(f"Campaign activated")
        return result

    def pause_campaign(self, campaign_id: str) -> dict:
        """Pause a running campaign."""
        return self._request("POST", f"/campaigns/{campaign_id}/pause")

    def get_campaign(self, campaign_id: str) -> dict:
        """Get campaign details."""
        return self._request("GET", f"/campaigns/{campaign_id}")

    def list_campaigns(self) -> dict:
        """List all campaigns."""
        return self._request("GET", "/campaigns")

    def get_campaign_analytics(self, campaign_id: str) -> dict:
        """Get campaign analytics."""
        return self._request("GET", f"/campaigns/{campaign_id}/analytics")

    # =========================================================================
    # LEAD ENDPOINTS
    # =========================================================================

    def add_leads_to_campaign(
        self,
        campaign_id: str,
        leads: List[dict],
        skip_if_in_workspace: bool = False
    ) -> dict:
        """
        Step 2: Add leads in bulk to a campaign with custom variables.

        Endpoint: POST /api/v2/leads/add

        Each lead must include custom_variables with:
        - email_body: The personalized email content
        - subject_variant_a, subject_variant_b, subject_variant_c: A/B/C subjects
        - follow_up_day_3: Day 3 follow-up body
        - follow_up_day_7: Day 7 follow-up body
        - problemAngle: For dynamic subject line in final email
        """
        payload = {
            "campaign_id": campaign_id,
            "leads": leads,
            "skip_if_in_workspace": skip_if_in_workspace
        }

        print(f"Adding {len(leads)} leads to campaign {campaign_id}")
        result = self._request("POST", "/leads/add", payload)
        print(f"Leads added: {result.get('added', 0)}, Duplicates: {result.get('duplicates', 0)}")
        return result

    def move_leads_to_campaign(
        self,
        campaign_id: str,
        lead_emails: List[str] = None,
        filter_type: str = None
    ) -> dict:
        """
        Move leads to a campaign (alternative to add_leads).

        Endpoint: POST /api/v2/leads/move

        Filter values:
        - FILTER_VAL_CONTACTED
        - FILTER_VAL_NOT_CONTACTED
        - FILTER_VAL_COMPLETED
        - FILTER_LEAD_INTERESTED
        - FILTER_LEAD_NOT_INTERESTED
        """
        payload = {
            "to_campaign_id": campaign_id
        }
        if lead_emails:
            payload["emails"] = lead_emails
        if filter_type:
            payload["filter"] = filter_type

        return self._request("POST", "/leads/move", payload)


# =============================================================================
# CAMPAIGN LAUNCHER
# =============================================================================

def format_lead_for_instantly(
    email: str,
    first_name: str,
    last_name: str,
    company_name: str,
    email_body: str,
    subject_variant_a: str,
    subject_variant_b: str,
    subject_variant_c: str,
    follow_up_day_3: str,
    follow_up_day_7: str,
    problem_angle: str
) -> dict:
    """
    Format a lead with custom variables for Instantly.

    Custom variables are used in the sequence templates:
    - {{email_body}} - Main email content
    - {{subject_variant_a/b/c}} - A/B/C testing subjects
    - {{follow_up_day_3}} - Day 3 follow-up content
    - {{follow_up_day_7}} - Day 7 follow-up content
    - {{problemAngle}} - For final email subject
    """
    return {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "company_name": company_name,
        "custom_variables": {
            "email_body": email_body,
            "subject_variant_a": subject_variant_a,
            "subject_variant_b": subject_variant_b,
            "subject_variant_c": subject_variant_c,
            "follow_up_day_3": follow_up_day_3,
            "follow_up_day_7": follow_up_day_7,
            "problemAngle": problem_angle
        }
    }


def launch_campaign(
    client: InstantlyClient,
    niche_name: str,
    problem_angle: str,
    leads_data: List[dict],
    from_emails: List[str],
    daily_limit: int = 25
) -> dict:
    """
    Launch a complete campaign for a niche.

    Steps:
    1. Create campaign with embedded sequences
    2. Add all leads with custom variables
    3. Activate campaign

    Returns campaign details including ID.
    """
    # Generate campaign name: {Niche}_{MonthYear}_{ProblemAngle}
    month_year = datetime.now().strftime("%b%Y")
    campaign_name = f"{niche_name}_{month_year}_{problem_angle}"

    print(f"\n{'='*60}")
    print(f"Launching campaign: {campaign_name}")
    print(f"{'='*60}")

    # Step 1: Create campaign with embedded sequences
    campaign = client.create_campaign(
        name=campaign_name,
        from_emails=from_emails,
        daily_limit=daily_limit
    )
    campaign_id = campaign.get("id")

    if not campaign_id:
        raise Exception("Failed to create campaign - no ID returned")

    # Step 2: Add leads with custom variables
    # Format leads for Instantly
    formatted_leads = []
    for lead in leads_data:
        formatted_leads.append(format_lead_for_instantly(
            email=lead["email"],
            first_name=lead["first_name"],
            last_name=lead.get("last_name", ""),
            company_name=lead["company_name"],
            email_body=lead["email_body"],
            subject_variant_a=lead["subject_variant_a"],
            subject_variant_b=lead["subject_variant_b"],
            subject_variant_c=lead["subject_variant_c"],
            follow_up_day_3=lead["follow_up_day_3"],
            follow_up_day_7=lead["follow_up_day_7"],
            problem_angle=lead.get("problemAngle", problem_angle)
        ))

    # Add leads in batches of 100 to avoid timeout
    batch_size = 100
    total_added = 0

    for i in range(0, len(formatted_leads), batch_size):
        batch = formatted_leads[i:i + batch_size]
        result = client.add_leads_to_campaign(campaign_id, batch)
        total_added += result.get("added", 0)
        time.sleep(0.5)  # Small delay between batches

    print(f"Total leads added: {total_added}")

    # Step 3: Activate campaign
    client.activate_campaign(campaign_id)

    print(f"\n✅ Campaign launched successfully!")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Campaign Name: {campaign_name}")
    print(f"   Leads: {total_added}")
    print(f"   Dashboard: https://app.instantly.ai/campaigns/{campaign_id}")

    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "leads_added": total_added,
        "status": "active"
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Launch campaigns for 3 niches

    # Initialize client
    # api_key = os.environ.get("INSTANTLY_API_KEY") or INSTANTLY_API_KEY
    # client = InstantlyClient(api_key)

    print("""
    Instantly Campaign Launcher
    ===========================

    This script creates campaigns with embedded 3-step sequences:
    - Email 1: Day 0 (3 subject variants for A/B/C testing)
    - Email 2: Day 3 (Follow-up)
    - Email 3: Day 7 (Final follow-up)

    Timezone: America/Los_Angeles (Pacific Time)

    Usage:
    1. Set INSTANTLY_API_KEY
    2. Load your leads from {niche}-emails.json
    3. Call launch_campaign() for each niche

    Example:

        client = InstantlyClient("your_api_key")

        result = launch_campaign(
            client=client,
            niche_name="Fire",
            problem_angle="AESForms",
            leads_data=leads,  # From fire-inspection-emails.json
            from_emails=["inbox1@domain.com", "inbox2@domain.com"]
        )
    """)
