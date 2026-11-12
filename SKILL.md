---
name: crm-contact-verification
description: >-
  Verify B2B CRM contacts by confirming each person's LinkedIn, current employer, and
  business email, then writing one status tag into the "Verified?" column. Use this
  skill WHENEVER the user uploads a contact list / CRM / lead list (Excel, CSV, or Google
  Sheets) with columns like LinkedIn URL, Company Name, Full Name, and Email and asks to
  "verify", "check", "validate", "clean", "enrich", or "tag" the contacts - even if they
  do not name this skill. Also trigger when the user references tags like "No Linkedin",
  "Resigned", or "No Valid Business Email found", or asks to confirm whether contacts
  still work somewhere or whether their emails are valid.
---

# CRM Contact Verification

Verify each contact and write exactly ONE tag into the "Verified?" column:
`No Linkedin` / `Resigned` / `No Valid Business Email found` / `Yes`.

Requires: a logged-in LinkedIn session in Chrome (via the Claude in Chrome tools) and the
email verifier at verifyemailaddress.org. Read `references/email-verification.md` before
the email phase - it has the SMTP codes, the probe-block test, and the Cloudflare
workaround that make this reliable. Read `references/company-matches.md` for parent/
subsidiary/renamed-company judgment calls.

## Setup (do first)
1. Read the input file (Excel/CSV/Sheets). Expected columns: Verified?, LinkedIn URL,
   Company Name, First Name, Last Name, Full Name, Email, Addl Email, Job Title
   (some may be missing; adapt).
2. Ask the user which rows to process if some are already tagged (only-blank vs all).
3. Connect Chrome and confirm LinkedIn is logged in. If multiple browsers are connected,
   ask the user which one.
4. Create a task list. Work in chunks (LinkedIn ~4/batch, email ~5-6/batch).

## Decision flow - evaluate STRICTLY top-down; first failure wins
Priority: No Linkedin > Resigned > No Valid Business Email found > Yes
(a higher check overrides a lower one even if the lower would pass).

### STEP 1 - LinkedIn
- If a URL is present, open it. Dead / 404 / redirect to bare /in/ -> treat as missing.
- If the URL is BLANK or was dead, SEARCH before concluding (mandatory - never tag
  "No Linkedin" just because the cell is empty or the link broke):
  1. LinkedIn people search "First Last Company"
  2. LinkedIn people search "First Last" + role keyword
  3. LinkedIn people search name only (scan results for the company)
  4. Name variants: accents (o-umlaut, o-slash, e-acute, n-tilde), maiden/married names,
     shortened display names ("Rene F."), middle names, initials
  5. Google: "First Last" Company linkedin
  - FOUND a plausible profile -> write the found/corrected URL back into the sheet, STEP 2.
  - NOT FOUND after all of the above -> tag No Linkedin. STOP.
- No Linkedin OVERRIDES a valid email. No findable profile = No Linkedin even if the
  email verifies valid.
- LinkedIn search result labels help: "Current: X at <co>" vs "Past: X at <co>".

### STEP 2 - Still at the CRM company?
- Read the profile CURRENT role (check Experience for dates; "Present" = current).
  Ignore keyword-stuffed headlines listing many past employers - confirm the real one.
- Current employer == CRM company, OR a known parent/subsidiary/renamed/acquired entity
  (see references/company-matches.md) -> go to STEP 3.
- Current employer is a DIFFERENT company -> tag Resigned. STOP.

### STEP 3 - Business email (must be SMTP-CONFIRMED valid)
- SMTP-verify the CRM email (see references/email-verification.md).
  - Confirmed VALID (SMTP 250) -> STEP 4 (=> Yes).
  - Not confirmed -> try to FIND a valid one: test Addl Email, generate & test format
    permutations (scripts/email_permutations.py), check renamed/acquired-company domains.
  - A found address that SMTP-confirms 250 -> write it to the sheet (Email column if
    blank; else Addl Email) -> STEP 4.
  - Nothing SMTP-confirms -> tag No Valid Business Email found. STOP.
- CRITICAL: "Yes" REQUIRES a mailbox that returns SMTP 250. These are all
  No Valid Business Email found:
  - blank email + none found
  - email present but server greylists (451/454) or blocks every probe
  - email present but confirmed invalid (550) + no working replacement
  Never tag "Yes" on a blank or unconfirmed email.

### STEP 4 - Yes
Only if: LinkedIn found + still at CRM company + email SMTP-250.

## Output
- Write ONE tag per row in Verified?, styled to match existing tag colors (copy
  font/fill/border/alignment from a reference row that already has that tag).
- Add an Email Status column after the last column for every row:
  Valid / Valid (found) / Invalid / Unverifiable - domain blocks probe /
  Inconclusive - greylisted / n/a (resigned) / No email in CRM.
- Write found LinkedIn URLs and found valid emails back into their columns.
- Add a short cell comment on any non-obvious row: resignations (name the new employer),
  renamed/acquired companies, found emails/URLs, probe-blocked domains, judgment calls.
- Do not overwrite the user other columns. Save as "<original name> - verified.xlsx"
  and share it. (Use the xlsx skill for openpyxl mechanics.)

## QA checklist - run BEFORE delivering
- [ ] Every Yes row has an email that returned SMTP 250.
- [ ] No Yes row has a blank or unconfirmed email.
- [ ] Every No Linkedin row was actually SEARCHED (LinkedIn + Google), not just blank URL.
- [ ] Every Resigned row names a different current employer in a comment.
- [ ] Every No Valid Business Email found row is LinkedIn-found + still employed.
- [ ] Exactly one tag per row; only the four allowed values used.
- [ ] Found URLs/emails written back; Email Status filled for all rows.

## Quick reference
```
Can't find on LinkedIn (after searching)      -> No Linkedin
Found, but now at a different company          -> Resigned
Found, employed, no SMTP-250 email             -> No Valid Business Email found
Found, employed, email SMTP 250                -> Yes
```
