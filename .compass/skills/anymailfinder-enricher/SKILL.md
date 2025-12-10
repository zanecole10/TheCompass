# ANYMAILFINDER DECISION-MAKER ENRICHER SKILL

## Purpose
Find verified decision-maker emails and full names using AnyMailFinder. Used for both Premium and Lite paths.

**CRITICAL:** Use AnyMailFinder for enrichment. Do NOT use Apify to enrich leads. Apify only scrapes company data from Google Maps. AnyMailFinder finds decision-maker emails and names.

**Key Change:** We use the **Decision Maker Search** endpoint to get the actual person's full name, email, and title.

## How to Use

**Script:** `.compass/scripts/anymailfinder_enricher.py`

```python
from anymailfinder_enricher import AnyMailFinderClient, enrich_leads, enrich_multiple_niches

# Initialize client with API key
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
```

**Key Features:**
- Saves progress after EVERY email found (won't lose work if interrupted)
- Can resume from where it left off automatically
- Handles rate limiting (1 request/second)
- Shows clear progress updates every 10 leads

**Output:** Saves to `{niche}-enriched.json`

**Expected find rate:** 50-60%

**Time:** ~1 second per lead (600 leads = ~10-15 minutes per niche)

## Trigger
- After Apify scraping completes
- "Enrich emails for {niche}"
- During Mission 2 lead acquisition phase

## Input
Company data from Apify (with website domains):
```json
{
  "companies": [
    {
      "company_name": "ACME HVAC Services",
      "website": "https://acmehvac.com",
      "location": "San Diego, CA",
      "rating": 4.8,
      "review_count": 47,
      "phone": "+1-619-555-0123"
    }
  ]
}
```

## Process

### Step 1: Extract Domain from Website

For each company, extract clean domain:
- `https://acmehvac.com` → `acmehvac.com`
- `http://www.acmehvac.com` → `acmehvac.com`
- Skip companies without website

### Step 2: Search for Decision-Maker via AnyMailFinder API

**API Endpoint:** POST https://api.anymailfinder.com/v5.0/search/decision-maker.json

```bash
curl -X POST "https://api.anymailfinder.com/v5.0/search/decision-maker.json" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "acmehvac.com",
    "decision_maker_category": "ceo"
  }'
```

**Required Parameters:**
- `domain`: Company website domain (e.g., "acmehvac.com")
- `decision_maker_category`: "ceo" (finds Owner, CEO, President, Founder)

**Response format:**
```json
{
  "email": "john@acmehvac.com",
  "personFullName": "John Smith",
  "personJobTitle": "Owner",
  "personLinkedinUrl": "https://linkedin.com/in/johnsmith"
}
```

**IMPORTANT Response Fields:**
- `email` → verified email address
- `personFullName` → full name (e.g., "Samuel Khodari") - split to get first name
- `personJobTitle` → title (e.g., "Owner", "Chairman and CEO")
- `personLinkedinUrl` → LinkedIn profile URL

### Step 3: Extract First Name from Full Name

Split `personFullName` to get the first name for email personalization:
- "Samuel Khodari" → first_name: "Samuel"
- "John Smith" → first_name: "John"
- "Mary Jane Watson" → first_name: "Mary"

Use only the first word before the space.

### Step 4: Batch Processing

- Process in batches of 50 companies
- Rate limit: 10 requests/second (AnyMailFinder API limit)
- Only charged for verified emails (95%+ confidence)
- Skip companies without website domain

### Step 5: Merge with Apify Data

Combine decision-maker data (from AnyMailFinder) with company data (from Apify):
```json
{
  "email": "john@acmehvac.com",
  "first_name": "John",
  "full_name": "John Smith",
  "title": "Owner",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "company_name": "ACME HVAC Services",
  "website": "https://acmehvac.com",
  "location": "San Diego, CA",
  "rating": 4.8,
  "review_count": 47,
  "phone": "+1-619-555-0123",
  "email_source": "anymailfinder",
  "enriched_at": "2025-11-24T10:30:00Z"
}
```

**Field mapping:**
- `email` ← AnyMailFinder `email`
- `first_name` ← First word of AnyMailFinder `personFullName`
- `full_name` ← AnyMailFinder `personFullName`
- `title` ← AnyMailFinder `personJobTitle`
- `linkedin_url` ← AnyMailFinder `personLinkedinUrl`
- `company_name`, `website`, `location`, `rating`, `review_count`, `phone` ← Apify data

### Step 6: Quality Filter

- Remove duplicates (same email address)
- Must have email and first_name (required for personalization)
- Skip entries where personFullName is empty or missing

## Expected Find Rate

**Target:** 50-60% of companies with websites

Why this rate:
- Not all companies have decision-maker emails publicly listed
- Some use personal emails (gmail, yahoo) that AnyMailFinder won't find
- Smaller companies less likely to have professional emails

**From 600 companies scraped per niche:**
- Expected: 300-360 decision-maker emails found
- This ensures minimum 75 emails per niche for campaign

## Output

Updates: `user-workspace/{niche-slug}-leads.json`

```json
{
  "niche": "hvac-inspection",
  "location": "California",
  "total_scraped": 600,
  "emails_found": 342,
  "find_rate": "57.0%",
  "decision_maker_breakdown": {
    "owner": 189,
    "ceo": 87,
    "president": 52,
    "founder": 14
  },
  "avg_confidence": 97.2,
  "cost": "$51.30",
  "enriched_at": "2025-11-24T10:45:00Z",
  "leads": [
    {
      "email": "john@acmehvac.com",
      "first_name": "John",
      "last_name": "Smith",
      "title": "Owner",
      "company_name": "ACME HVAC Services",
      "location": "San Diego, CA",
      "rating": 4.8,
      "review_count": 47,
      "confidence": 98,
      "email_source": "anymailfinder"
    }
  ]
}
```

## Example Output (Console)

```
✅ DECISION-MAKER ENRICHMENT COMPLETE: HVAC Inspection

Companies scraped: 600
Decision-maker emails found: 342 (57.0% find rate)
Verified confidence: 97.2% average

Decision-maker breakdown:
- Owners: 189 (55.3%)
- CEOs: 87 (25.4%)
- Presidents: 52 (15.2%)
- Founders: 14 (4.1%)

Cost: $51.30 ($0.15 per email)

Sample enriched leads:
1. John Smith - Owner @ ACME HVAC (john@acmehvac.com) ✓ 98%
2. Sarah Johnson - CEO @ Elite HVAC (sarah@elitehvac.com) ✓ 97%
3. Mike Davis - President @ ProHVAC (mdavis@prohvac.com) ✓ 99%

📁 Updated: hvac-inspection-leads.json

Ready to write personalized emails using decision-maker first names.
```

## Error Handling

**No website available:**
```
⚠️ No website for {company_name} - skipping enrichment
```

**API rate limit hit:**
```
⏳ Rate limit reached - waiting 10 seconds before continuing...
```

**Low find rate (<40%):**
```
⚠️ LOW ENRICHMENT RATE

Found only {X} emails from {Y} companies (Z% find rate).
Expected: 50-60% find rate

Possible causes:
- Many companies without professional websites
- Industry uses personal emails (gmail, yahoo)
- Company domains not properly extracted

Recommendations:
- Continue if {X} > 75 emails (minimum for campaign)
- Try broader location if below minimum
- Check that Apify scraped companies with websites

Continue with {X} decision-maker emails? (yes/no)
```

**AnyMailFinder API error:**
```
❌ ANYMAILFINDER API ERROR

Error: {error_message}

Possible causes:
- Invalid API key
- API credits exhausted
- AnyMailFinder service issue

Check your account: https://anymailfinder.com/dashboard

Retrying... (Attempt 1 of 2)
```

After 2nd failure:
```
❌ ENRICHMENT FAILED (2 attempts)

Unable to enrich: {niche}

Actions:
1. Verify API key is valid
2. Check AnyMailFinder credits
3. Try again in a few minutes

Continue with other niches? (yes/no)
```

## Cost Tracking

Update `mission-2-costs.json`:
```json
{
  "anymailfinder_searches": 600,
  "anymailfinder_emails_found": 342,
  "anymailfinder_cost": 51.30,
  "cost_per_email": 0.15,
  "find_rate": "57.0%"
}
```

## API Documentation

**Endpoint:** POST https://api.anymailfinder.com/v5.0/search/decision-maker.json

**Required Parameters:**
- `domain`: Company website domain
- `decision_maker_category`: "ceo" (finds Owner, CEO, President, Founder)

**Response Fields:**
- `email`: Verified email address
- `personFullName`: Full name (e.g., "Samuel Khodari")
- `personJobTitle`: Title (e.g., "Owner", "Chairman and CEO")
- `personLinkedinUrl`: LinkedIn profile URL

**Pricing:** ~$0.15 per verified email found
**Rate limit:** 10 requests/second
**Plan needed:** $49/month for 500 searches

## Notes

- **CRITICAL:** Use AnyMailFinder for enrichment. Do NOT use Apify to enrich leads.
- Apify = scrapes company data from Google Maps (company_name, website, rating, etc.)
- AnyMailFinder = finds decision-maker email and full name
- **Decision Maker Search** returns `personFullName` - split to get first name
- First name used for email personalization: "{{firstName}}"
- Higher quality leads (decision-makers more likely to respond)
- 50-60% find rate is expected and acceptable
- Both Premium and Lite paths use this
- Process takes 10-15 minutes for 600 companies per niche
