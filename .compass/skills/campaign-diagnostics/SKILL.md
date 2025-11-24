## Purpose
Analyze campaign performance across 3 niches, identify winning niche, provide statistical confidence, recommend next steps.

## Trigger
- "Run diagnostics"
- "Check campaign data"
- "Show results"
- "Which niche won?"

## Prerequisites

Minimum thresholds:
- At least 5 days of sending
- At least 8 total replies
- At least 200 total emails sent

If below:
```
📊 DIAGNOSTICS NOT READY

Current:
- Days: {X} (need 5+)
- Replies: {Y} (need 8+)
- Sent: {Z} (need 200+)

Need more data. Check back in {days}.

Current snapshot (insufficient):
- HVAC: {sent} sent, {replies} replies
- Fire: {sent} sent, {replies} replies
- PropMgmt: {sent} sent, {replies} replies
```

## Data Collection

Fetch from Instantly API:
```bash
curl -X GET https://api.instantly.ai/v1/campaigns/{id}/stats \
  -H "Authorization: Bearer {API_KEY}"
```

Collect per campaign:
- Total sent
- Total opens
- Total replies
- Positive replies (interested)
- Neutral replies (questions)
- Negative replies (not interested)
- Bounce rate
- Spam report rate

## Analysis Framework

### 1. Open Rate
```
Open Rate = (Opens / Sent) × 100
```

Benchmarks:
- 40-60%: Good
- 30-40%: Acceptable
- Under 30%: Deliverability issue

### 2. Reply Rate
```
Reply Rate = (Replies / Sent) × 100
```

Benchmarks:
- 5-10%: Excellent
- 3-5%: Good
- 1-3%: Acceptable
- Under 1%: Poor fit

### 3. Interest Rate (KEY)
```
Interest Rate = (Interested / Sent) × 100
```

Interested = Positive replies asking for demo, info, pricing

Benchmarks:
- 2-4%: Excellent
- 1-2%: Good
- 0.5-1%: Acceptable
- Under 0.5%: Poor fit

### 4. Winner Identification

Ranking criteria:
1. Interest rate (most important)
2. Reply rate (engagement)
3. Open rate (deliverability)

Statistical confidence:
```
If winner's interest rate is:
- 2x+ other niches: HIGH confidence
- 1.5-2x others: MEDIUM confidence
- 1.0-1.5x others: LOW confidence
```

## Output Format

Create: `user-workspace/mission-2-checkpoint.md`

```markdown
# MISSION 2 CHECKPOINT - CAMPAIGN DIAGNOSTICS

**Analysis Date:** 2025-11-27
**Days Sending:** 7
**Total Sent:** 582

---

## RESULTS BY NICHE

### 🥇 WINNER: Fire Inspection (AES Forms)

**Performance:**
- Sent: 203
- Opens: 112 (55.2%)
- Replies: 14 (6.9%)
- **Interested: 7 (3.4%)** ⭐
- Not interested: 5 (2.5%)
- Questions: 2 (1.0%)

**Interested Prospects:**
1. John Smith @ ABC Fire - "Show me a demo"
2. Sarah Johnson @ Elite Fire - "How much?"
3. Mike Davis @ ProFire - "Can this work for us?"
4. Lisa Chen @ SafeGuard Fire - "Book a call"
5. Tom Wilson @ FireGuard Plus - "Send more info"
6. Amy Martinez @ FirstLine Fire - "When can you demo?"
7. Chris Taylor @ Apex Fire - "This could save us hours"

**Why it won:**
- 3.4% interest rate (2x higher)
- 6.9% reply rate (strong engagement)
- 55% open rate (good deliverability)
- Problem resonates strongly

---

### 🥈 Second: HVAC Inspection (Job Costing)

**Performance:**
- Sent: 186
- Opens: 89 (47.8%)
- Replies: 7 (3.8%)
- **Interested: 3 (1.6%)**
- Not interested: 3 (1.6%)
- Questions: 1 (0.5%)

**Interested Prospects:**
1. Bob Anderson @ ACME HVAC - "Tell me more"
2. Karen White @ Elite HVAC - "Interested"
3. David Brown @ ProHVAC - "Book demo"

**Analysis:**
- 1.6% interest rate (half of Fire)
- Acceptable but less urgent

---

### 🥉 Third: Property Management

**Performance:**
- Sent: 193
- Opens: 83 (43.0%)
- Replies: 5 (2.6%)
- **Interested: 2 (1.0%)**
- Not interested: 2 (1.0%)
- Questions: 1 (0.5%)

**Interested Prospects:**
1. Jennifer Lee @ Property Masters - "Can this integrate?"
2. Robert Garcia @ MegaManage - "Show me how"

**Analysis:**
- 1.0% interest rate (lowest)
- Problem less acute

---

## STATISTICAL CONFIDENCE

**Winner: Fire Inspection**
**Confidence: HIGH ✅**

Interest rate (3.4%) is 2.1x HVAC (1.6%) and 3.4x PropMgmt (1.0%).

With 7 interested from 203 emails, statistically significant.

---

## OVERALL CAMPAIGN HEALTH

**Deliverability:** ✅ Good
- Avg open rate: 48.7%
- Bounce rate: 1.2%
- Spam reports: 0

**Engagement:** ✅ Strong
- Avg reply rate: 4.5%
- Avg interest rate: 2.1%

**Email Quality:** ✅ Excellent
- Personalization working
- Problem angles resonate
- No spam filter issues

---

## RECOMMENDED NEXT STEPS

### 1. Focus on Fire Inspection

**Immediate:**
1. Reply to 7 interested prospects within 24 hours
2. Book discovery calls
3. Use Mission 3 scripts

**Scaling:**
1. Send 500 more emails to Fire niche
2. Refine copy based on replies
3. Target sub-niches

### 2. Handle Other Niches

**HVAC:**
- 1.6% acceptable
- Keep as backup
- Run 200 more to confirm

**PropMgmt:**
- 1.0% too low
- Pause and research different angle

### 3. Enter Mission 3

**Objective:** Convert interested to booked calls

**You have 7 warm leads ready.**

Start Mission 3: "Begin Mission 3"

---

## FILES CREATED

✅ 3 niches researched (Mission 1)
✅ 582 emails sent (Mission 2)
✅ 12 interested prospects
✅ 1 clear winner (Fire Inspection)

**Mission 2 complete.** 🎉

Time to book calls. 🧭
```

## Display Summary

After checkpoint:
```
🎉 MISSION 2 COMPLETE - RESULTS READY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇 WINNER: Fire Inspection
   - 3.4% interest (7 prospects)
   - HIGH confidence (2x+ others)

🥈 HVAC Inspection
   - 1.6% interest (3 prospects)

🥉 Property Management
   - 1.0% interest (2 prospects)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Full analysis: mission-2-checkpoint.md

🎯 NEXT: Reply to 7 Fire prospects, book calls.

Ready for Mission 3? "Begin Mission 3"
```

## Notes
- Don't run before minimums met
- Interest rate is THE key metric
- Winner must be 1.5x+ for confidence
- Show all interested prospect names
- Recommend next steps based on data
```
