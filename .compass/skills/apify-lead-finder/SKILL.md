# APIFY LEAD FINDER SKILL

## Purpose
Scrape Google Maps for companies in specified niche and location using Apify's Google Maps Scraper. For Budget path, Apify returns basic contact data. For Premium path, scraping only (AnyMailFinder handles enrichment).

## Trigger
- "Find leads for {niche}"
- "Scrape {niche} companies"
- During Mission 2 launch sequence

## Input
```json
{
  "niche": "HVAC inspection companies",
  "location": "California",
  "limit": 300,
  "path": "premium" | "budget"
}
```

## Process

### Step 1: Scrape Google Maps via Apify

Call Apify API to run Google Maps Scraper actor:
```bash
curl -X POST https://api.apify.com/v2/acts/nwua9Gu5YrADL7ZDj/runs \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "searchStringsArray": ["{niche} in {location}"],
    "maxCrawledPlacesPerSearch": 300,
    "language": "en",
    "includeWebsites": true,
    "includeEmails": true,
    "includePhones": true
  }'
```

Returns (from Apify):
- Company name
- Address
- Phone number
- Website
- Email (if publicly available on Google Maps)
- Rating
- Review count
- Categories
- Opening hours

**Cost:** $0.004 per place = ~$1.20 for 300 companies (covered by $5 free monthly credits)

### Step 2: Wait for Scraper to Complete

Poll the run status:
```bash
curl https://api.apify.com/v2/acts/nwua9Gu5YrADL7ZDj/runs/{RUN_ID} \
  -H "Authorization: Bearer {API_KEY}"
```

Wait until status = "SUCCEEDED"

### Step 3: Retrieve Results

Get dataset items:
```bash
curl https://api.apify.com/v2/acts/nwua9Gu5YrADL7ZDj/runs/{RUN_ID}/dataset/items \
  -H "Authorization: Bearer {API_KEY}"
```

### Step 4: Process & Clean Data

For Budget path (no AnyMailFinder):
- Extract email field from Apify results (if available)
- Expected find rate: 30-40% (Google Maps public emails)

For Premium path:
- Store company data without emails
- AnyMailFinder will enrich in next skill
- Expected find rate after enrichment: 60-70%

Quality checks:
- Remove duplicates (same company name + location)
- Remove generic emails (info@, contact@, sales@) for Budget path
- Prefer personal emails over generic
- Validate email format

### Step 5: Output

Save to: `user-workspace/{niche-slug}-leads.json`

```json
{
  "niche": "HVAC inspection",
  "location": "California",
  "total_found": 287,
  "emails_found": 102,
  "find_rate": "35.5%",
  "cost": "$1.15",
  "path": "budget",
  "scraped_at": "2025-11-20T10:30:00Z",
  "apify_run_id": "abc123xyz",
  "leads": [
    {
      "company_name": "ACME HVAC Services",
      "location": "San Diego, CA",
      "address": "123 Main St, San Diego, CA 92101",
      "email": "john@acmehvac.com",
      "phone": "+1-619-555-0123",
      "website": "https://acmehvac.com",
      "rating": 4.8,
      "review_count": 47,
      "categories": ["HVAC contractor", "Air conditioning repair"],
      "hours": "Mon-Fri: 8am-6pm"
    }
  ]
}
```

## Thresholds & Warnings

**Minimum per niche:** 75 companies scraped

**If 20-75 companies:**
```
⚠️ LOW COMPANY COUNT

Found only {X} companies for {Niche}. Recommended minimum: 75.

Suggestions:
- Try broader location (e.g., "California" → "West Coast")
- Try related search terms
- Premium path gets 2x email find rate with AnyMailFinder

Continue with {X} companies? (yes/no)
```

**If below 20:**
```
❌ INSUFFICIENT DATA

Only {X} companies for {Niche}. Too low for testing.

Recommendations:
1. Change search terms
2. Expand location (try statewide or multi-state)
3. Try different niche
4. Upgrade to Premium path for better email enrichment

Cannot launch with under 20 companies.
```

## Error Handling

**API credits exhausted:**
```
💳 APIFY CREDITS EXHAUSTED

Need {X} more credits to complete.

Current usage: ${used} of $5 free credits
Additional needed: ${needed}

[Add credits](https://console.apify.com/billing)

Options:
1. Continue with {Y} companies scraped (type 'continue')
2. Stop and add credits (type 'stop')
```

**Scraper run failed:**
```
❌ APIFY SCRAPER FAILED

Error: {error_message}

Possible causes:
- Invalid search query
- Apify service issue
- API key invalid

Retrying... (Attempt 1 of 2)
```

After 2nd failure:
```
❌ FAILED (2 attempts)

Unable to scrape: {niche}

Actions:
1. Check Apify dashboard: https://console.apify.com/actors/runs
2. Verify API key is valid
3. Try different search terms

Continue with other niches? (yes/no)
```

## Example Output

```
✅ LEAD SCRAPING COMPLETE: HVAC Inspection

Companies found: 287
Emails found: 102 (35.5% find rate)
Cost: $1.15 (within $5 free credits)

Sample leads:
1. John Smith - Owner @ ACME HVAC (john@acmehvac.com)
2. Sarah Johnson - President @ Elite HVAC (sarah@elitehvac.com)
3. Mike Davis - CEO @ ProHVAC (mdavis@prohvac.com)

📁 Saved to: hvac-leads.json

Ready for email enrichment (Premium) or email writing (Budget).
```

## API Documentation

- Apify Google Maps Scraper: https://apify.com/scrapers/google-maps
- Actor ID: `nwua9Gu5YrADL7ZDj`
- Pricing: $0.004 per place (pay-per-event)
- Free credits: $5/month on Starter plan
- Expected scraping time: 2-5 minutes for 300 places

## Notes

- Apify's scraper is faster than manual scraping (2X speed)
- Returns structured JSON data immediately
- Includes public emails when available on Google Maps listings
- No rate limiting issues (Apify handles proxy rotation)
- Budget path gets ~30-40% email find rate from Google Maps data
- Premium path + AnyMailFinder achieves ~60-70% email find rate
