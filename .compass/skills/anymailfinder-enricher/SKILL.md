# ANYMAILFINDER ENRICHER SKILL

## Purpose
Enrich company data with verified email addresses using AnyMailFinder. **PREMIUM PATH ONLY.**

## Trigger
- After AirScale scraping (Premium path only)
- "Enrich {niche} with emails"

## Input
Company data from AirScale (no emails yet):
```json
{
  "companies": [
    {
      "company_name": "ACME HVAC Services",
      "website": "acmehvac.com",
      "location": "San Diego, CA",
      "phone": "+1-619-555-0123"
    }
  ]
}
```

## Process

### Step 1: Call AnyMailFinder API

For each company:
```bash
curl -X POST https://api.anymailfinder.com/v4.0/search/company \
  -H "Authorization: Bearer {API_KEY}" \
  -d '{
    "company_name": "ACME HVAC Services",
    "company_domain": "acmehvac.com",
    "role": "owner"
  }'
```

### Step 2: Batch Processing
- Process in batches of 50
- Only charged for verified emails (97%+ confidence)
- Skip if no website available

### Step 3: Merge with AirScale Data
```json
{
  "company_name": "ACME HVAC Services",
  "email": "john@acmehvac.com",
  "first_name": "John",
  "last_name": "Smith",
  "title": "Owner",
  "confidence": 98,
  "source": "anymailfinder",
  ...original_data
}
```

### Step 4: Quality Filter
- Only keep 97%+ confidence
- Remove duplicates
- Prefer decision-makers

## Output

Updates: `user-workspace/{niche-slug}-leads.json`

Adds `email_source` field: "anymailfinder"

## Example Output

```
✅ EMAIL ENRICHMENT COMPLETE: HVAC Inspection

Companies processed: 287
Emails found: 186 (64.8% find rate)
Verified emails: 186 (97%+ confidence)
Cost: $28.50

Find rate: 35.5% (AirScale) → 64.8% (+ AnyMailFinder)

Sample enriched:
1. John Smith - Owner @ ACME HVAC (john@acmehvac.com) ✓ 98%
2. Sarah Johnson - President @ Elite HVAC (sarah@elitehvac.com) ✓ 97%
3. Mike Davis - CEO @ ProHVAC (mdavis@prohvac.com) ✓ 99%

📁 Updated: hvac-leads.json

Ready to write emails.
```

## Cost Tracking

Update `mission-2-costs.json`:
```json
{
  "anymailfinder_enrichments": 186,
  "anymailfinder_cost": 28.50,
  "cost_per_email": 0.153
}
```
