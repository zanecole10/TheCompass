# INSTANTLY CAMPAIGN LAUNCHER SKILL

## Purpose
Create and launch email campaigns in Instantly with embedded 3-step sequences, A/B testing, and bulk lead upload.

**CRITICAL:** Use Instantly V2 API only. API docs: https://developer.instantly.ai/api/v2

**Script:** `.compass/scripts/instantly_campaign_launcher.py`

## How to Use

This skill uses the Python script at `.compass/scripts/instantly_campaign_launcher.py` to launch campaigns.

### Running the Script

```bash
# Set API key first
export INSTANTLY_API_KEY="your_api_key_here"

# Run the script
python .compass/scripts/instantly_campaign_launcher.py
```

### Programmatic Usage

```python
from instantly_campaign_launcher import InstantlyClient, launch_campaign

# Initialize client
client = InstantlyClient(api_key)

# Launch campaign
result = launch_campaign(
    client=client,
    niche_name="Fire",
    problem_angle="AESForms",
    leads_data=leads,  # From {niche}-emails.json
    from_emails=["inbox1@domain.com", "inbox2@domain.com"]
)

print(f"Campaign ID: {result['campaign_id']}")
print(f"Leads added: {result['leads_added']}")
```

## Trigger
- After email approval
- "Launch campaigns"
- User types "LAUNCH" then "CONFIRM"

## Input
```json
{
  "niche": "HVAC inspection",
  "problem_angle": "JobCosting",
  "emails": [...], // from email-writer-professional skill
  "inboxes": ["inbox1@domain1.com", "inbox2@domain1.com"],
  "path": "premium" | "lite"
}
```

## Campaign Configuration

### Naming
```
{Niche}_{Month}{Year}_{ProblemAngle}
```

Examples:
- `HVAC_Nov2025_JobCosting`
- `Fire_Nov2025_AESForms`
- `PropMgmt_Nov2025_ComplianceTracking`

### Sending Limits
- **Daily:** 25 emails per inbox
- **Per campaign:** 50 emails/day (2 inboxes)
- **All campaigns:** 150 emails/day total (3 niches × 50)
- **Timeline:** ~600 emails ÷ 150/day = 4-5 days

### Settings
- Stop on reply: YES
- Stop on out-of-office: YES
- Track opens: YES
- Track clicks: YES
- Include unsubscribe: YES (required)
- Timezone: `Etc/GMT+12` (Instantly required format - set in script)

## 3-Step Email Sequence

**Email 1 (Initial) - Day 0:**
- Send immediately
- A/B testing: 3 subject variants (33% each)
- Body: Main email from {{email_body}}
- Subject: {{subject_variant_a}}, {{subject_variant_b}}, {{subject_variant_c}}

**Email 2 (Follow-up) - Day 3:**
- Send if no reply after 3 days
- Subject: `Re: {{subject_variant_a}}`
- Body: {{follow_up_day_3}}

**Email 3 (Final Follow-up) - Day 7:**
- Send 4 days after Email 2 (Day 7 total)
- Subject: `Last note - {{problem_angle}}`
- Body: {{follow_up_day_7}}

## CRITICAL: Custom Variable Naming Convention

**All custom variables MUST use snake_case (lowercase with underscores).**

| Variable | Format | Example |
|----------|--------|---------|
| email_body | snake_case ✅ | `{{email_body}}` |
| subject_variant_a | snake_case ✅ | `{{subject_variant_a}}` |
| subject_variant_b | snake_case ✅ | `{{subject_variant_b}}` |
| subject_variant_c | snake_case ✅ | `{{subject_variant_c}}` |
| follow_up_day_3 | snake_case ✅ | `{{follow_up_day_3}}` |
| follow_up_day_7 | snake_case ✅ | `{{follow_up_day_7}}` |
| problem_angle | snake_case ✅ | `{{problem_angle}}` |

**DO NOT USE camelCase for custom variables:**
- ❌ `emailBody` - WRONG
- ❌ `subjectVariantA` - WRONG
- ❌ `followUpDay3` - WRONG
- ❌ `problemAngle` - WRONG

**Why this matters:** The campaign template uses `{{email_body}}`. If leads are uploaded with `emailBody`, the variable won't match and emails will show the raw placeholder instead of the content.

**Built-in Instantly variables (use as-is):**
- `{{firstName}}` - Lead's first name
- `{{lastName}}` - Lead's last name
- `{{companyName}}` - Lead's company
- `{{sendingAccountFirstName}}` - Sender's first name (signature)

## Inbox Distribution

- Campaign 1 (Niche 1): Inbox 1 + Inbox 2
- Campaign 2 (Niche 2): Inbox 3 + Inbox 4
- Campaign 3 (Niche 3): Inbox 5 + Inbox 6

## Pre-Launch: Lite Path Warmup Check

**IMPORTANT:** If Lite path, verify warmup using V2 API before launching.

### Check Warmup Status

```bash
curl -X GET https://api.instantly.ai/v2/account/emails \
  -H "Authorization: Bearer {API_KEY}"
```

Parse response for each inbox and verify:
- **Status:** Active
- **Days warming:** 21+
- **Daily warmup emails:** 10-20

If ANY inbox under 21 days:
```
❌ INBOXES NOT READY

Inbox: contact@domain1.com
Warmed: 14 days (need 21+)

Warmup schedule:
- Week 1: 5-10 emails/day
- Week 2: 10-15 emails/day
- Week 3: 15-20 emails/day
- Week 4+: Ready (25/day)

Launch available in 7 days.

[Check status](https://app.instantly.ai/inboxes)
```

Block launch if under 21 days. Premium path skips this check (pre-warmed).

## V2 API Implementation

**Base URL:** https://api.instantly.ai

### Step 1: Create Campaign with Embedded Sequences

**Endpoint:** POST /api/v2/campaigns

```bash
curl -X POST "https://api.instantly.ai/api/v2/campaigns" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json"
```

**Request:**
```json
{
  "name": "HVAC_Nov2025_JobCosting",
  "campaign_schedule": {
    "schedules": [
      {
        "name": "HVAC_Nov2025_JobCosting Schedule",
        "timing": {
          "from": "09:00",
          "to": "17:00"
        },
        "days": {
          "monday": true,
          "tuesday": true,
          "wednesday": true,
          "thursday": true,
          "friday": true,
          "saturday": false,
          "sunday": false
        },
        "timezone": "Etc/GMT+12"
      }
    ]
  },
  "from_emails": ["inbox1@domain1.com", "inbox2@domain1.com"],
  "daily_limit": 25,
  "stop_on_reply": true,
  "stop_on_auto_reply": true,
  "track_opens": true,
  "track_clicks": true,
  "sequences": [
    {
      "steps": [
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
        {
          "type": "email",
          "delay": 4,
          "variants": [
            {
              "subject": "Last note - {{problem_angle}}",
              "body": "{{follow_up_day_7}}"
            }
          ]
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "id": "camp_abc123",
  "name": "HVAC_Nov2025_JobCosting",
  "status": "paused",
  "created_at": "2025-11-24T10:30:00Z"
}
```

**Store campaign_id for Step 2.**

### Step 2: Upload Leads with Custom Variables

**Endpoint:** POST /api/v2/leads/add

```bash
curl -X POST "https://api.instantly.ai/api/v2/leads/add" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json"
```

**Request:**
```json
{
  "campaign_id": "camp_abc123",
  "leads": [
    {
      "email": "john@acmehvac.com",
      "first_name": "John",
      "last_name": "Smith",
      "company_name": "ACME HVAC Services",
      "custom_variables": {
        "email_body": "John,\n\nSaw ACME HVAC Services has 4.8 stars...",
        "subject_variant_a": "4 hours on job costing???",
        "subject_variant_b": "HVAC job costing nightmare???",
        "subject_variant_c": "John, quick HVAC question",
        "follow_up_day_3": "John,\n\nFollowing up on my email...",
        "follow_up_day_7": "John,\n\nLast email, I promise...",
        "problem_angle": "Job Costing"
      }
    }
  ],
  "skip_if_in_workspace": false
}
```

**Important:**
- `custom_variables` contains ALL email content (body + 3 subjects + 2 follow-ups)
- Variables referenced in sequences are replaced at send time
- `skip_if_in_workspace: false` allows duplicate emails across campaigns

**Response:**
```json
{
  "added": 186,
  "duplicates": 0,
  "invalid": 0
}
```

### Step 3: Activate Campaign

**Endpoint:** POST /api/v2/campaigns/{campaign_id}/activate

```bash
curl -X POST "https://api.instantly.ai/api/v2/campaigns/{campaign_id}/activate" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json"
```

**Alternative (PATCH):** PATCH /api/v2/campaigns/{campaign_id}
```json
{
  "status": "active"
}
```

Campaign starts sending within 1 hour.

## Complete Launch Process

### Pre-Launch Checklist

Before launching, verify:
```
✅ API key configured
✅ Domains purchased (3)
✅ Inboxes connected (6)
✅ Inboxes warmed 21+ days (Lite only)
✅ Leads scraped (600 per niche)
✅ Emails enriched (~300-360 per niche)
✅ Emails written with approval
✅ Campaign names formatted correctly
```

### Launch Sequence

1. **Show summary** when user types "LAUNCH":
```
🚀 READY TO LAUNCH

Campaign 1: HVAC_Nov2025_JobCosting
- Leads: 342
- Inboxes: inbox1@domain1.com, inbox2@domain1.com
- Sending: 50 emails/day
- Est. complete: 7 days

Campaign 2: Fire_Nov2025_AESForms
- Leads: 298
- Inboxes: inbox3@domain2.com, inbox4@domain2.com
- Sending: 50 emails/day
- Est. complete: 6 days

Campaign 3: PropMgmt_Nov2025_ComplianceTracking
- Leads: 315
- Inboxes: inbox5@domain3.com, inbox6@domain3.com
- Sending: 50 emails/day
- Est. complete: 6 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 955 leads
Daily: 150 emails/day
Timeline: ~6-7 days to complete

Sequences:
- Email 1: Immediate (3 subject A/B variants)
- Email 2: Day 3 follow-up
- Email 3: Day 7 final follow-up

Type "CONFIRM" to launch all 3 campaigns.
```

2. **Execute** when user types "CONFIRM":
   - Create Campaign 1 with sequences
   - Upload leads for Campaign 1
   - Activate Campaign 1
   - Create Campaign 2 with sequences
   - Upload leads for Campaign 2
   - Activate Campaign 2
   - Create Campaign 3 with sequences
   - Upload leads for Campaign 3
   - Activate Campaign 3

3. **Create tracking file:** `mission-2-progress.md`

4. **Display success**

## Error Handling

### Campaign Creation Fails

```
❌ CAMPAIGN LAUNCH FAILED

Campaign: HVAC_Nov2025_JobCosting
Error: {error_message}

Possible causes:
- Invalid API key
- Inbox not connected
- Daily limit exceeded
- Invalid campaign name format

[Instantly Support](https://help.instantly.ai)

Retrying... (Attempt 1 of 2)
```

After 2nd failure:
```
❌ FAILED (2 attempts)

Unable to create: HVAC_Nov2025_JobCosting

Actions:
1. Check Instantly dashboard
2. Verify inbox connections
3. Try manual creation

Continue with other campaigns? (yes/no)
```

### Lead Upload Fails

```
❌ LEAD UPLOAD FAILED

Campaign: HVAC_Nov2025_JobCosting
Error: {error_message}

Possible causes:
- Invalid email format
- Custom variable names mismatch
- API rate limit

Retrying... (Attempt 1 of 2)
```

### API Rate Limit

```
⏳ RATE LIMIT HIT

Instantly API rate limit reached.
Waiting 60 seconds before continuing...
```

## Output

Success message:
```
✅ CAMPAIGN LAUNCHED: HVAC_Nov2025_JobCosting

Details:
- 342 leads uploaded
- 3 subject variants (A/B testing)
- Follow-ups: Day 3, Day 7
- Sending: 25/day × 2 inboxes = 50/day
- Start: Within 1 hour
- Est. complete: 7 days

📊 Dashboard: https://app.instantly.ai/campaigns/camp_abc123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CAMPAIGN LAUNCHED: Fire_Nov2025_AESForms

Details:
- 298 leads uploaded
- 3 subject variants (A/B testing)
- Follow-ups: Day 3, Day 7
- Sending: 25/day × 2 inboxes = 50/day
- Start: Within 1 hour
- Est. complete: 6 days

📊 Dashboard: https://app.instantly.ai/campaigns/camp_def456

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CAMPAIGN LAUNCHED: PropMgmt_Nov2025_ComplianceTracking

Details:
- 315 leads uploaded
- 3 subject variants (A/B testing)
- Follow-ups: Day 3, Day 7
- Sending: 25/day × 2 inboxes = 50/day
- Start: Within 1 hour
- Est. complete: 6 days

📊 Dashboard: https://app.instantly.ai/campaigns/camp_ghi789

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 ALL 3 CAMPAIGNS LAUNCHED!

Total leads: 955
Emails per day: 150
Est. completion: 6-7 days

Emails begin sending within 1 hour.
Check stats in Instantly dashboard.

Type "Show Mission 2 status" anytime to check progress.
```

Update `mission-2-progress.md`:
```markdown
## Campaign Status

### HVAC_Nov2025_JobCosting
- Status: Active 🟢
- Campaign ID: camp_abc123
- Leads: 342
- Sent: 0 (starting soon)
- Opens: 0
- Replies: 0
- Interested: 0
- Launched: 2025-11-24 10:45 AM
- Dashboard: https://app.instantly.ai/campaigns/camp_abc123

### Fire_Nov2025_AESForms
- Status: Active 🟢
- Campaign ID: camp_def456
- Leads: 298
- Sent: 0 (starting soon)
- Opens: 0
- Replies: 0
- Interested: 0
- Launched: 2025-11-24 10:46 AM
- Dashboard: https://app.instantly.ai/campaigns/camp_def456

### PropMgmt_Nov2025_ComplianceTracking
- Status: Active 🟢
- Campaign ID: camp_ghi789
- Leads: 315
- Sent: 0 (starting soon)
- Opens: 0
- Replies: 0
- Interested: 0
- Launched: 2025-11-24 10:47 AM
- Dashboard: https://app.instantly.ai/campaigns/camp_ghi789

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All campaigns launched successfully!

Check status: "Show Mission 2 status"
Run diagnostics (after 5+ days): "Run diagnostics"
```

## Instantly V2 API Reference

**Base URL:** https://api.instantly.ai
**Docs:** https://developer.instantly.ai/api/v2

### Campaign Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/campaigns | Create campaign (with embedded sequences) |
| GET | /api/v2/campaigns | List campaigns |
| GET | /api/v2/campaigns/{id} | Get campaign details |
| PATCH | /api/v2/campaigns/{id} | Update campaign |
| POST | /api/v2/campaigns/{id}/activate | Activate (start) campaign |
| POST | /api/v2/campaigns/{id}/pause | Pause campaign |
| DELETE | /api/v2/campaigns/{id} | Delete campaign |

### Lead Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/leads/add | Add leads to campaign (bulk) |
| POST | /api/v2/leads/move | Move leads to campaign/list |
| GET | /api/v2/leads | List leads |
| PATCH | /api/v2/leads/{id} | Update lead |
| DELETE | /api/v2/leads/{id} | Delete lead |

### Subsequence Endpoints (Alternative to embedded sequences)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v2/subsequences | Create campaign subsequence |
| GET | /api/v2/subsequences | List subsequences |
| PATCH | /api/v2/subsequences/{id} | Update subsequence |
| DELETE | /api/v2/subsequences/{id} | Delete subsequence |

### Analytics Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v2/campaigns/{id}/analytics | Get campaign analytics |
| GET | /api/v2/campaigns/{id}/analytics/overview | Get analytics overview |

## Notes

- **Script location:** `.compass/scripts/instantly_campaign_launcher.py`
- **V2 API only** - Do not use V1 endpoints
- **Sequences embedded** in campaign creation (not added separately)
- **Custom variables** store all email content for dynamic insertion
- **Timezone:** `Etc/GMT+12` (Instantly required format - configured in script)
- **A/B testing:** 3 variants in step 1, each gets 33% traffic
- **Delays are RELATIVE to previous step** (not cumulative from start):
  - Email 1: delay: 0 → Day 0
  - Email 2: delay: 3 → 3 days after Email 1 = Day 3
  - Email 3: delay: 4 → 4 days after Email 2 = Day 7
- **Stop on reply:** Automatically stops sequence if lead replies
- **Campaign IDs:** Store for analytics and status checks
- **Launch timing:** Campaigns start sending within 1 hour of activation
- **Batch processing:** Script uploads leads in batches of 100 to avoid timeouts
