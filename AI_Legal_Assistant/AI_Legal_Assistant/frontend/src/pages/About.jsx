export default function About() {
  return (
    <section>
      <h1>About</h1>
      <div className="info-card">
        <p>
          This hackathon project demonstrates Retrieval-Augmented Generation
          (RAG) for Indian legal information.
        </p>
        <h3>Architecture</h3>
        <p>Documents → Cleaning → Chunking → Embeddings → FAISS → Retrieval → LLM → Sources</p>
        <h3>Important</h3>
        <p>
          It is an educational prototype and must not be presented as a
          substitute for professional legal advice.
        </p>
      </div>
    </section>
  );
}
