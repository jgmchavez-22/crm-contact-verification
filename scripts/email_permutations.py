#!/usr/bin/env python3
"""Generate common business-email format permutations for a person at a domain.

Usage:
    python email_permutations.py "First Last" domain.com
    python email_permutations.py "Anne-Eva Sparf Aagaard" nilfisk.com

Prints one candidate address per line, most-common formats first. Feed these to the
SMTP verifier (verifyemailaddress.org) and keep the first that returns SMTP 250.

Notes:
- Nordic / German / most EU corporates use first.last@domain -> try it first.
- Some use first-initial + lastname (jgill@, hpetersen@, mkinateder@).
- Strip accents to ASCII (o-umlaut->o, e-acute->e, etc.).
- For compound/particle surnames (van, de, von) try both joined and separated forms.
"""
import sys, unicodedata, re

def ascii_fold(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z]", "", s).lower()

def permutations(full_name, domain):
    parts = [p for p in re.split(r"\s+", full_name.strip()) if p]
    if len(parts) < 2:
        first = ascii_fold(parts[0]); last = first
    else:
        first = ascii_fold(parts[0]); last = ascii_fold(parts[-1])
    f, l = first[:1], last[:1]
    joined_last = ascii_fold("".join(parts[1:]))  # for particle/compound surnames
    templates = [
        f"{first}.{last}", f"{f}.{last}", f"{f}{last}", f"{first}{last}",
        f"{first}_{last}", f"{first}-{last}", f"{last}.{first}", f"{last}{first}",
        f"{first}", f"{last}", f"{first}.{l}", f"{first}{l}", f"{l}.{first}",
        f"{last}.{f}", f"{last}{f}", f"{f}.{l}", f"{f}{l}",
        f"{first}.{joined_last}", f"{f}.{joined_last}", f"{first}{joined_last}",
    ]
    seen, out = set(), []
    for lp in templates:
        e = f"{lp}@{domain}"
        if lp and e not in seen:
            seen.add(e); out.append(e)
    return out

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    for e in permutations(sys.argv[1], sys.argv[2]):
        print(e)
