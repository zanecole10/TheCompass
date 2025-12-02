# PROFESSIONAL EMAIL WRITER SKILL

## Purpose
Write personalized, high-converting cold emails using the 7-Part Email Framework. Quality standard: Indistinguishable from 20-year professional copywriter.

## ⚠️ CRITICAL: ANTI-HALLUCINATION RULES

**ONLY use data you ACTUALLY have from Apify:**
- ✅ Company name
- ✅ Location (city, state)
- ✅ Rating (e.g., 4.8 stars)
- ✅ Review count (e.g., 47 reviews)
- ✅ Website, phone, categories

**NEVER guess or fabricate:**
- ❌ Their volume (calls/week, inspections/month)
- ❌ Their team size
- ❌ Their revenue
- ❌ Number of units/properties
- ❌ Specific operational details

**Use industry averages, not fake specifics.**

## The 7-Part Email Framework

Every email follows this exact structure:

1. **Subject Line** - Stop the scroll (shocking question or stat)
2. **Hook** - Compliment/Recognition using REAL data (2-3 sentences)
3. **Problem Statement** - Specific industry pain question (1-2 sentences)
4. **Make It Real** - Industry averages, quantify pain (2-3 sentences)
5. **Solution Tease** - Show there's a better way (2 sentences)
6. **Social Proof** - Generic industry reference (1 sentence)
7. **Call to Action** - Ultra casual, low pressure (1 sentence)
8. **Signature** - Simple sign-off using sending account first name

**Total length:** 120-180 words (excluding signature)

## Before Writing: Load Context

**CRITICAL:** Load Mission 1 research first:

```
user-workspace/{niche-slug}-research.md
user-workspace/{niche-slug}-problems.md
user-workspace/{niche-slug}-opportunities.md
user-workspace/{niche-slug}-avatar.md
```

Extract:
- Their exact language for pain points
- Industry terminology
- Industry-wide time waste (not specific to one company)
- Current bad solutions
- What the industry wishes existed

## Personalization Variables

For EACH lead (from Apify data):
- `{{firstName}}` - First name (decision-maker from AnyMailFinder)
- `{{companyName}}` - Company name
- `{{location}}` - City, State
- `{{rating}}` - Star rating (e.g., 4.8)
- `{{reviewCount}}` - Number of reviews (e.g., 47)
- `{{industry}}` - Industry type
- `{{state}}` - State name
- `{{city}}` - City name

From research (industry-wide, not company-specific):
- `{{painPhrase}}` - Exact pain from research
- `{{industryTimeWaste}}` - Industry average time waste
- `{{problem_angle}}` - Problem being solved

From Instantly (automatically populated):
- `{{sendingAccountFirstName}}` - First name of sending account (for signature)

## PART 1: SUBJECT LINE

### Formula 1: Shocking Time Question
```
{{Hours}} on {{painPhrase}}???
```

Examples:
- "4 hours on AES forms???"
- "10-day deadline???"
- "$5,000 fine???"

### Formula 2: Shocking Percentage/Cost
```
{{Percentage}}% {{problem}}???
```

Examples:
- "30% ticketing fees???"
- "8% on every ticket???"

### Formula 3: Time/Cost Comparison (Not Recommended - Skip)

**Generate 2-3 subject variants for A/B testing.**

Rules:
- ✅ Use shocking stats from research
- ✅ End with "???" for emphasis
- ✅ Keep under 40 characters
- ✅ Use THEIR language from research
- ❌ NO "Hope this finds you well"
- ❌ NO "Partnership opportunity"

## PART 2: HOOK (Compliment/Recognition)

Use ONLY real Apify data to compliment or recognize them.

### Formula 1: Rating + Reviews Compliment
```
{{firstName}},

Saw {{companyName}} has {{rating}} stars with {{reviewCount}} reviews in {{city}} - nice work. {{industry}} in {{state}} is competitive.
```

Example:
```
Andrew,

Saw Chivalry has 4.8 stars with 120 reviews in LA - nice work. Live music venues in California are competitive.
```

### Formula 2: Achievement Recognition (If Data Available)
```
{{firstName}},

Love what you're doing out in {{city}} with {{companyName}}. {{Observation from public data}}. {{Compliment}}.
```

Example:
```
Andrew,

Love what you're doing out in LA with Chivalry. Just saw you had your 9 year anniversary. Huge congrats man, that's something to be proud of. Especially in a competitive spot like LA.
```

### Formula 3: Simple Recognition
```
{{firstName}},

Saw {{companyName}} does {{industry}} in {{city}}. {{Compliment about their work}}.
```

Example:
```
John,

Saw ACME Backflow does backflow testing in Sacramento. Respect - that's detail-oriented work.
```

Rules:
- ✅ ONLY use data from Apify (rating, reviews, location)
- ✅ Sound genuine and conversational
- ✅ Compliment something specific
- ✅ 2-3 sentences
- ❌ NO generic "I came across your company"
- ❌ NO "Hope this email finds you well"
- ❌ NO guessing their achievements

## PART 3: PROBLEM STATEMENT

Ask a specific question about their industry pain.

### Formula:
```
Quick question: Are you {{specific pain from research}}?
```

Examples:

**Fire Inspection:**
```
Quick question: Are you still spending hours on California Title 19 AES forms after every inspection?
```

**Backflow Testing:**
```
Quick question: Are you dealing with that new 10-day submission deadline California just rolled out?
```

**Venues:**
```
Quick question: I saw you're using DICE for ticketing. Are you currently paying 7-8% on every single ticket?
```

**Property Management:**
```
Quick question: Are you tracking fire, backflow, elevator, and pool inspections across your portfolio in spreadsheets?
```

Rules:
- ✅ Use exact pain from Mission 1 research
- ✅ Be specific to their industry
- ✅ Reference current/recent problems
- ✅ 1-2 sentences max
- ❌ NO guessing their specific situation
- ❌ NO generic "Do you struggle with X?"

## PART 4: MAKE IT REAL

Quantify the pain using INDUSTRY AVERAGES (not their specific data).

### Formula:
```
Most {{industry}} companies {{time/cost waste}}. {{Visceral impact}}.
```

Examples:

**Fire Inspection:**
```
Most fire protection companies waste 15-20 hours a week just on AES paperwork and manual invoicing. That adds up fast.
```

**Backflow Testing:**
```
Most backflow testing companies spend 20-30 minutes per test just on water district paperwork. When you're doing hundreds of tests a month, that's basically a full-time job.
```

**Venues:**
```
You sell all 2,000 tickets at $50, but DICE takes 8-9% on every single ticket (yikes).

That means you're paying $8,000-$9,000 in JUST fees. That's equal to ALL of your profit for one of your smaller shows. Gone.
```

**Property Management:**
```
Most property managers spend 5-10 hours a month manually tracking compliance. And one missed inspection can mean thousands in fines.
```

Rules:
- ✅ Use industry averages from research
- ✅ Quantify time OR money waste
- ✅ Make it visceral ("basically a full-time job")
- ✅ 2-3 sentences
- ❌ NEVER guess their specific volume
- ❌ NO "For a company doing 80 calls/week" (you don't know!)
- ❌ NO "With 500 units" (you don't know!)

## PART 5: SOLUTION TEASE

Show there's a better way without explaining HOW.

### Formula:
```
What if {{transformation}}? I {{built/created}} {{solution description}}.
```

Examples:

**Fire Inspection:**
```
What if you could cut that time by 75%? I built something specifically for California fire companies that handles AES forms automatically.
```

**Backflow Testing:**
```
What if you could cut that time to 5 minutes per test? I built something that auto-fills water district forms and tracks the 10-day deadline automatically.
```

**Venues:**
```
What if I told you that you could cut your ticketing fees by 70% immediately and instead KEEP that profit? I actually built a solution for mid-sized venues just like you, that allow you to lose the ridiculous fees and take home more.
```

**Property Management:**
```
What if you never missed another deadline? I built a system that automatically tracks every inspection across your portfolio and sends reminders 90/60/30 days out.
```

Rules:
- ✅ Start with "What if"
- ✅ State clear transformation (% or time saved)
- ✅ "I built" or "I created" (personal)
- ✅ 2 sentences
- ❌ NO feature lists
- ❌ NO technical jargon
- ❌ NO "Our platform offers..."

## PART 6: SOCIAL PROOF

Generic industry reference (you have NO clients yet, or only 1-3).

### Formula 1: Industry Average Savings
```
{{Industry}} companies {{doing similar work}} are {{outcome}}.
```

Examples:

**Fire Inspection:**
```
Other fire companies in California are saving 10-15 hours a week by automating their paperwork.
```

**Backflow Testing:**
```
Other testing companies are saving 15-20 hours a week on paperwork alone.
```

**Venues:**
```
Similar sized venues to you in the LA area usually make an extra $5,000-$6,000 per show by switching to their OWN platform and abandoning the blood sucking ticketing platforms.
```

**Property Management:**
```
Property managers using this stopped waking up at 3am worried about what's overdue.
```

### Formula 2: Specific Client (ONLY if you have permission)
```
{{Client name}} is now {{outcome}}.
```

Example:
```
The Crystal Ballroom out in Portland is now making an extra $10,000-$12,000 PER SHOW by using a system like this.
```

Rules:
- ✅ Keep it vague and believable
- ✅ Focus on emotional outcomes when possible
- ✅ Use "other companies" not client names
- ✅ 1 sentence
- ❌ NO specific client names without permission
- ❌ NO unbelievable numbers ("save $1M")
- ❌ NO "Companies using our platform..."

## PART 7: CALL TO ACTION

Ultra casual, low pressure.

### Recommended CTAs:
```
Worth {{low time}} to see if {{conditional}}?
```

Examples:
- "Worth 15 minutes to see if it'd work for {{companyName}}?"
- "Worth a quick call this week to walk through it?"
- "Quick call this week to see if it fits?"

### Alternative Casual:
- "Wanna see how it works?"
- "Let me know if you want to see it"
- "I just found a problem in your market, I built a cool thing to solve it, and I thought it might help you"

Rules:
- ✅ Keep it casual and conversational
- ✅ Low time commitment
- ✅ Make it conditional ("see if")
- ✅ 1 sentence
- ❌ NO "Want to see it?" (too generic per user request)
- ❌ NO "Schedule a demo" (too formal)
- ❌ NO "Book a call" (too salesy)

## PART 8: SIGNATURE

Simple, casual sign-off using the sending account's first name.

### Formula:
```
{{sendingAccountFirstName}}
```

**CRITICAL:** Use the variable `{{sendingAccountFirstName}}` exactly as shown. This is automatically populated by Instantly with the first name from the sending email account.

Examples of what will appear:
- If sending from john@domain.com → "John"
- If sending from sarah@domain.com → "Sarah"

Rules:
- ✅ Use ONLY `{{sendingAccountFirstName}}` variable
- ✅ No last name needed
- ✅ No title, company, or contact info
- ✅ Keep it minimal and personal
- ❌ NO "Best regards" or "Sincerely"
- ❌ NO company signature blocks
- ❌ NO phone numbers or links in signature

## COMPLETE EMAIL EXAMPLES

### Example 1: Fire Inspection

**Subject:** 4 hours on AES forms???

**Body:**

{{firstName}},

Saw {{companyName}} has {{rating}} stars with {{reviewCount}} reviews in {{city}} - nice work. Fire protection in California is competitive.

Quick question: Are you still spending hours on California Title 19 AES forms after every inspection?

Most fire protection companies waste 15-20 hours a week just on AES paperwork and manual invoicing. That adds up fast.

What if you could cut that time by 75%? I built something specifically for California fire companies that handles AES forms automatically.

Other fire companies in California are saving 10-15 hours a week by automating their paperwork.

Worth 15 minutes to see if it'd work for {{companyName}}?

{{sendingAccountFirstName}}

**Word count:** 120

---

### Example 2: Backflow Testing

**Subject:** 10-day deadline???

**Body:**

{{firstName}},

Saw {{companyName}} does backflow testing in {{city}}. Respect - that's detail-oriented work.

Quick question: Are you dealing with that new 10-day submission deadline California just rolled out?

Most backflow testing companies spend 20-30 minutes per test just on water district paperwork. When you're doing hundreds of tests a month, that's basically a full-time job.

What if you could cut that time to 5 minutes per test? I built something that auto-fills water district forms and tracks the 10-day deadline automatically.

Other testing companies are saving 15-20 hours a week on paperwork alone.

Quick call this week to see if it fits?

{{sendingAccountFirstName}}

**Word count:** 118

---

### Example 3: Property Management

**Subject:** $5,000 fine???

**Body:**

{{firstName}},

Noticed {{companyName}} manages properties in {{city}} - solid {{rating}} star rating.

Quick question: Are you tracking fire, backflow, elevator, and pool inspections across your portfolio in spreadsheets?

Most property managers spend 5-10 hours a month manually tracking compliance. And one missed inspection can mean thousands in fines.

What if you never missed another deadline? I built a system that automatically tracks every inspection across your portfolio and sends reminders 90/60/30 days out.

Property managers using this stopped waking up at 3am worried about what's overdue.

Worth a quick call this week to walk through it?

{{sendingAccountFirstName}}

**Word count:** 115

## Tone Guidelines

**DO:**
- ✅ Sound conversational (like a friend)
- ✅ Short sentences (10-15 words max)
- ✅ Use contractions
- ✅ Be direct and honest
- ✅ Sound curious, not pushy
- ✅ Use "you" more than "I" or "we"
- ✅ Read naturally out loud

**DON'T:**
- ❌ Sound corporate or formal
- ❌ Use jargon or buzzwords
- ❌ Sound desperate or salesy
- ❌ Multiple exclamation points
- ❌ Sound robotic
- ❌ Passive voice
- ❌ "Hope this email finds you well"

## Quality Checklist

Before outputting ANY email:

### Data Usage:
- [ ] Used ONLY real Apify data (rating, reviews, location)
- [ ] Did NOT guess volume, team size, or revenue
- [ ] Used industry averages from research, not fake specifics
- [ ] Mentioned company name + location with real data

### Framework Compliance:
- [ ] All 8 parts present
- [ ] Subject line is shocking question/stat
- [ ] Hook uses real compliment/recognition
- [ ] Problem statement is specific to industry
- [ ] Make It Real uses industry averages only
- [ ] Solution tease starts with "What if"
- [ ] Social proof is generic industry reference
- [ ] CTA is casual and low-pressure
- [ ] Signature uses {{sendingAccountFirstName}}

### Quality:
- [ ] Length 120-180 words
- [ ] Reads naturally out loud
- [ ] No jargon or corporate speak
- [ ] Would I believe this if I received it?
- [ ] Would I respond to this?

## Follow-Up Sequences

### Email 2 (Day 3)

**Subject:** `Re: {{original_subject}}`

```
{{firstName}},

Following up on my email from {{dayOfWeek}}.

Still curious if {{companyName}} has found a better way to handle {{problem_angle}} yet?

Most {{industry}} companies we talk to didn't realize there was a faster way until we showed them.

Worth a quick call this week?

{{sendingAccountFirstName}}
```

### Email 3 (Day 7)

**Subject:** `Last note - {{problem_angle}}`

```
{{firstName}},

Last email, I promise.

If {{companyName}} isn't dealing with {{problem_angle}} anymore, great - you can ignore this.

But if you're still {{painfulTask}}, I built something that might save your team {{industryTimeSavings}}.

Let me know if you want to see it. Otherwise, I'll stop bugging you.

{{sendingAccountFirstName}}
```

## Output Format

Save to: `user-workspace/{niche-slug}-emails.json`

**CRITICAL: Use snake_case for ALL custom variable names. DO NOT use camelCase.**

| Correct (snake_case) | WRONG (camelCase) |
|---------------------|-------------------|
| `email_body` | ~~emailBody~~ |
| `subject_variant_a` | ~~subjectVariantA~~ |
| `follow_up_day_3` | ~~followUpDay3~~ |
| `problem_angle` | ~~problemAngle~~ |

```json
{
  "niche": "fire-inspection",
  "total_emails": 203,
  "campaign_angle": "AESForms",
  "subject_variants": [
    "4 hours on AES forms???",
    "California Title 19???",
    "{{firstName}}, AES form question"
  ],
  "emails": [
    {
      "email": "john@abcfire.com",
      "first_name": "John",
      "company_name": "ABC Fire Protection",
      "location": "San Diego, CA",
      "rating": 4.8,
      "review_count": 47,
      "subject_variant_a": "4 hours on AES forms???",
      "subject_variant_b": "California Title 19???",
      "subject_variant_c": "John, AES form question",
      "email_body": "[Personalized email using ONLY real data]",
      "follow_up_day_3": "[Day 3 follow-up email]",
      "follow_up_day_7": "[Day 7 follow-up email]",
      "problem_angle": "AES Forms",
      "word_count": 120,
      "framework_check": {
        "subject_line": true,
        "hook": true,
        "problem_statement": true,
        "make_it_real": true,
        "solution_tease": true,
        "social_proof": true,
        "call_to_action": true,
        "signature": true
      },
      "data_validation": {
        "used_real_data_only": true,
        "no_guessed_volume": true,
        "industry_averages_only": true
      }
    }
  ]
}
```

## Notes

- Load research BEFORE writing
- Extract THEIR industry phrases
- Use REAL data for personalization (rating, reviews, location)
- Use INDUSTRY AVERAGES for pain quantification
- NEVER guess their specific operations
- Keep it conversational and human
- Read out loud - if robotic, rewrite
- Short sentences (10-15 words)
- Their language > your language

**Goal: Emails so good they seem like they came from someone who actually researched them and genuinely wants to help.**
