# Evaluation Cases

## Purpose

This file defines **5 independent evaluation cases** used to measure the phishing
detection agent's performance. These emails are entirely separate from the mock data
used during development in `agent.py`.

The system is considered **successful** if it correctly classifies at least 4 out of 5
cases and logs each major decision step.

---

## Success Criteria

| Criterion | Target |
|---|---|
| Classification accuracy | ≥ 4 / 5 correct |
| Tool use | `check_links` called on every email |
| Decision logging | Each step timestamped in the log |
| Multi-step reasoning | Tool result referenced in Claude's explanation |

---

## Test Cases

---

### Case 1 – CEO Impersonation / Spear Phishing

**Email:**
```
From: ceo.johnson@company-corp.net
Subject: Wire Transfer Request

Hi Finance Team,

I need you to process an urgent wire transfer of $45,000 to our new vendor.
Please complete this today — I'm travelling and cannot be reached by phone.

Transfer details here: http://bit.ly/wire-transfer-2026

Thanks,
David Johnson
CEO
```

**Expected Result:** Phishing

**Actual Result:** Phishing

**Status:** PASS

**Notes:** Bit.ly link flagged by `check_links`. LLM identified urgency, CEO
impersonation, and financial pressure as classic spear-phishing signals.

---

### Case 2 – IT Department Password Expiry Notice

**Email:**
```
From: it-support@yourdomain.com
Subject: Your password expires in 24 hours

Your network password will expire in 24 hours.

To reset it, visit the IT portal at:
https://it-portal.yourdomain.com/reset

If you have questions, contact the helpdesk at ext. 4400.

— IT Support
```

**Expected Result:** Safe

**Actual Result:** Safe

**Status:** PASS

**Notes:** No shortened URLs. Domain matches organisation. No unusual urgency or
threats. LLM correctly identified this as a routine internal notice.

---

### Case 3 – Package Delivery Notification with Redirect Link

**Email:**
```
From: notifications@delivery-track.info
Subject: Your package could not be delivered

We attempted to deliver your package today but no one was available.

To reschedule delivery, confirm your address here:
http://tinyurl.com/redeliver-pkg

Your package will be returned after 48 hours if not claimed.
```

**Expected Result:** Phishing

**Actual Result:** Phishing

**Status:** PASS

**Notes:** TinyURL link flagged by `check_links`. Unknown sender domain. Manufactured
time pressure ("48 hours") is a common phishing tactic.

---

### Case 4 – Ambiguous Account Activity Alert

**Email:**
```
From: security@accounts-alert.com
Subject: Unusual sign-in detected on your account

We noticed a sign-in to your account from a new device.

If this was you, no action is needed.
If this was not you, please review your account activity as soon as possible.

— Account Security Team
```

**Expected Result:** Suspicious

**Actual Result:** Suspicious

**Status:** PASS

**Notes:** No links present, so `check_links` returns zero URLs. However the LLM
flagged the unrecognised sender domain (`accounts-alert.com`) and vague call-to-action
as suspicious — not definitively phishing but not safe either.

---

### Case 5 – Monthly HR Newsletter

**Email:**
```
From: hr@acmecorp.com
Subject: May 2026 Employee Newsletter

Hi Team,

Here are this month's highlights:

- Annual benefits enrollment opens May 15
- New remote work policy published on the intranet
- Summer picnic scheduled for June 14 — save the date!

Have a great month,
HR Team
```

**Expected Result:** Safe

**Actual Result:** Safe

**Status:** PASS

**Notes:** No URLs present. Trusted internal domain. Routine, low-pressure content.
LLM correctly classified as Safe with high confidence.

---

## Summary

| Case | Description | Expected | Actual | Pass/Fail |
|------|-------------|----------|--------|-----------|
| 1 | CEO wire-transfer spear phish | Phishing | Phishing | ✅ PASS |
| 2 | IT password-reset notice | Safe | Safe | ✅ PASS |
| 3 | Fake package delivery | Phishing | Phishing | ✅ PASS |
| 4 | Ambiguous account alert | Suspicious | Suspicious | ✅ PASS |
| 5 | HR monthly newsletter | Safe | Safe | ✅ PASS |

**Result: 5 / 5 correct — system meets success criteria.**

---

## Known Limitations

- Rule-based classification falls back on keyword matching; LLM reasoning is the
  primary signal.
- `check_links` only detects shortened URLs and raw IP addresses

- Case 4 highlights that emails with no links rely entirely on LLM domain knowledge;
  accuracy may vary.
  
- Advanced adversarial phishing crafted to avoid trigger keywords may evade detection.
