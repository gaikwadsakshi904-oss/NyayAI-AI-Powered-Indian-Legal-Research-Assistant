LEGAL_KEYWORDS = {
    "consumer", "contract", "notice", "refund", "complaint",
    "law", "legal", "act", "rule", "regulation", "rights"
}

def is_legal_question(question):
    q = question.lower()
    return any(word in q for word in LEGAL_KEYWORDS)

def safety_message():
    return (
        "I can help with general legal information and explain documents. "
        "I cannot replace a qualified lawyer or provide a guaranteed legal outcome."
    )
