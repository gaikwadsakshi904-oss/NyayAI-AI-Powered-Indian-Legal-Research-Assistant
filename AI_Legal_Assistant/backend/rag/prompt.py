SYSTEM_PROMPT = """
You are an Indian legal information assistant.
Use only the supplied context when making factual legal claims.
Explain legal concepts in simple language.
Never pretend to be a lawyer, court, or government authority.
If the context does not contain the answer, say that the available sources
are insufficient and suggest checking an official source or consulting a lawyer.
Do not invent sections, case numbers, deadlines, penalties, or citations.
"""

def build_prompt(question, contexts):
    context_text = "\n\n".join(
        f"[Source {i+1}: {c['metadata']['source']}]\n{c['text']}"
        for i, c in enumerate(contexts)
    )
    return f"""{SYSTEM_PROMPT}

CONTEXT:
{context_text}

QUESTION:
{question}

Answer with:
1. Short answer
2. Relevant legal information from the context
3. Sources used
4. A brief note that this is general legal information, not legal advice.
"""
