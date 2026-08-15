from config import TOP_K
from rag.retriever import retrieve
from rag.prompt import build_prompt
from llm.llm import generate

DISCLAIMER = (
    "This tool provides general legal information, not legal advice. "
    "For important or disputed matters, consult a qualified lawyer."
)

def answer_question(question):
    contexts = retrieve(question, TOP_K)

    if not contexts:
        return {
            "answer": "No indexed legal sources were found. Please add official legal documents and build the index.",
            "sources": [],
            "disclaimer": DISCLAIMER
        }

    prompt = build_prompt(question, contexts)
    answer = generate(prompt)

    if not answer:
        answer = (
            "I found these relevant legal sources, but the local language model is not running. "
            "Start Ollama and install the configured model, then ask again."
        )

    sources = [
        {
            "source": c["metadata"]["source"],
            "path": c["metadata"]["path"],
            "score": round(c["score"], 3),
            "excerpt": c["text"][:300] + ("..." if len(c["text"]) > 300 else "")
        }
        for c in contexts
    ]

    return {"answer": answer, "sources": sources, "disclaimer": DISCLAIMER}
