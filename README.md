# CRM Contact Verification & Email Permutations

> An automated B2B contact verification framework, AI agent skill, and corporate email permutation generator that validates employment records, standardizes multi-jurisdiction domain patterns, and verifies deliverability against live SMTP servers.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![AI Agent Skill](https://img.shields.io/badge/Skill-Antigravity%20%7C%20Agentic-purple?style=flat)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

---

## 📋 Overview

### The Challenge
Lead generation, CRM enrichment, and outbound sales pipelines waste significant time and incur email bounce penalties when sending messages to outdated or incorrectly formatted contacts. B2B databases frequently contain:
- Discontinued roles or resigned personnel.
- Broken or inaccurate LinkedIn profiles.
- Unpredictable corporate email patterns (e.g., `first.last`, `f.last`, `firstlast`, joined particle surnames).

### The Solution
This repository provides:
1. **Deterministic Email Permutation Generator (`scripts/email_permutations.py`):** Produces ranked corporate email patterns ordered by empirical enterprise frequency, handling compound surnames (`van`, `de`, `von`) and Unicode/diacritic normalization.
2. **AI Agent Skill Specification (`SKILL.md`):** A strict hierarchical decision flow (`No Linkedin` > `Resigned` > `No Valid Business Email found` > `Yes`) for automated agents verifying CRM lead lists.
3. **Reference Guides (`references/`):** Comprehensive procedures for SMTP response codes, catch-all server detection, and parent/subsidiary corporate hierarchy resolution.

---

## 🏛️ Repository Structure

```
crm-contact-verification/
├── SKILL.md                          # Standardized Agentic Skill definition & workflow
├── scripts/
│   └── email_permutations.py         # Standalone corporate email permutation CLI
├── references/
│   ├── email-verification.md         # SMTP status code guide & mail exchanger checks
│   └── company-matches.md            # Corporate structure & subsidiary mapping rules
├── .gitignore                        # Git exclusion rules
└── README.md                         # Technical overview and documentation
```

---

## 🚀 Usage

### Email Permutation Generator (CLI)

Generate candidate email permutations ordered from most common to least common formats:

```bash
python scripts/email_permutations.py "First Last" domain.com
```

**Example:**
```bash
python scripts/email_permutations.py "Anne-Eva Sparf Aagaard" example.com
```

**Output:**
```text
anne-eva.aagaard@example.com
a.aagaard@example.com
aaagaard@example.com
anne-evaaagaard@example.com
anne-eva_aagaard@example.com
...
```

### Agentic Skill Integration

To use as an agent skill within Antigravity or compatible AI agent frameworks:
- Copy `crm-contact-verification` into your workspace `.gemini/antigravity/skills/` or global skills directory.
- The agent activates the skill whenever lead lists or CRM spreadsheets require verification or deliverability validation.

---

## 🛠️ Tech Stack

- **Scripting:** Python 3.8+ (Zero external dependencies — uses Python standard library `unicodedata`, `re`, `sys`)
- **Agent Protocol:** Antigravity / Claude Agent Skill Standard (`SKILL.md` frontmatter)
