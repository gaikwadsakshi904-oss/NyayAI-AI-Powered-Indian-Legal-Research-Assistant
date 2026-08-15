from document_analysis.clause_extractor import extract_clauses

RISK_WORDS = [
    "penalty", "unlimited liability", "automatic renewal",
    "non-refundable", "exclusive jurisdiction", "indemnify"
]

def analyze_contract(text):
    clauses = extract_clauses(text)
    lower = text.lower()
    risks = []

    for word in RISK_WORDS:
        if word.lower() in lower:
            risks.append({
                "term": word,
                "message": f"Potentially important clause detected: {word}."
            })

    return {
        "summary": "The document was processed and potentially important clauses were extracted.",
        "clauses": clauses,
        "risks": risks,
        "disclaimer": (
            "This analysis is for general information only and is not a legal opinion."
        )
    }
