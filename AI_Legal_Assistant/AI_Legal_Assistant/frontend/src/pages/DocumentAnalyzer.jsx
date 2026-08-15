import { useState } from "react";
import FileUpload from "../components/FileUpload";

export default function DocumentAnalyzer() {
  const [result, setResult] = useState(null);

  return (
    <section>
      <h1>Document Analyzer</h1>
      <p className="lead">Upload a contract or notice to extract important clauses.</p>
      <FileUpload onResult={setResult} />

      {result?.error && <div className="error">{result.error}</div>}

      {result && !result.error && (
        <div className="analysis">
          <h2>Summary</h2>
          <p>{result.summary}</p>

          <h2>Detected Clauses</h2>
          {result.clauses?.length
            ? result.clauses.map((c, i) => (
                <div className="result-card" key={i}>
                  <strong>{c.type}</strong>
                  <p>{c.text}</p>
                </div>
              ))
            : <p>No predefined clauses detected.</p>}

          <h2>Potentially Important Terms</h2>
          {result.risks?.length
            ? result.risks.map((r, i) => (
                <div className="risk" key={i}>⚠️ {r.message}</div>
              ))
            : <p>No predefined risk terms detected.</p>}
        </div>
      )}
    </section>
  );
}
