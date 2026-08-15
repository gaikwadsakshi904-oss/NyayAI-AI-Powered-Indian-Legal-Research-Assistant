import re

CLAUSE_PATTERNS = {
    "termination": r"\btermination\b|\bterminate\b",
    "payment": r"\bpayment\b|\bfee\b|\bprice\b",
    "confidentiality": r"\bconfidential\b|\bconfidentiality\b",
    "liability": r"\bliability\b|\bliable\b",
    "dispute_resolution": r"\barbitration\b|\bdispute resolution\b",
    "jurisdiction": r"\bjurisdiction\b|\bgoverning law\b",
    "notice": r"\bnotice\b",
    "refund": r"\brefund\b|\breimbursement\b"
}

def extract_clauses(text):
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    found = []
    for name, pattern in CLAUSE_PATTERNS.items():
        matches = [p for p in paragraphs if re.search(pattern, p, re.I)]
        if matches:
            found.append({
                "type": name,
                "text": " ".join(matches[:3])
            })
    return found
