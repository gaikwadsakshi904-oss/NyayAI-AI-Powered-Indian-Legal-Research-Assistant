export default function Dashboard({ setPage }) {
  return (
    <section>
      <h1>AI Legal Assistant</h1>
      <p className="lead">
        Search Indian legal documents, ask questions, and analyze contracts
        using a source-grounded RAG system.
      </p>

      <div className="cards">
        <button onClick={() => setPage("chat")}>
          <h2>💬 Legal Chat</h2>
          <p>Ask questions in simple language and view supporting sources.</p>
        </button>
        <button onClick={() => setPage("analyzer")}>
          <h2>📄 Document Analyzer</h2>
          <p>Upload a contract and identify important clauses and risks.</p>
        </button>
        <button onClick={() => setPage("sources")}>
          <h2>📚 Legal Sources</h2>
          <p>Use official documents as the knowledge base.</p>
        </button>
      </div>
    </section>
  );
}
