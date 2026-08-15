DISCLAIMER = (
    "Disclaimer: NyayAI provides AI-assisted legal information "
    "for research and educational purposes only. It does not "
    "constitute professional legal advice. For case-specific "
    "legal matters, consult a qualified legal professional."
)


def add_disclaimer(answer: str) -> str:

    if not answer:
        answer = "No answer was generated."

    return f"{answer}\n\n{DISCLAIMER}"
