import { useState } from "react";
import { analyzeDocument } from "../services/api";

export default function FileUpload({ onResult }) {
  const [loading, setLoading] = useState(false);

  async function upload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      onResult(await analyzeDocument(file));
    } catch (err) {
      onResult({ error: err.response?.data?.detail || "Upload failed." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <label className="upload">
      <input type="file" accept=".pdf,.txt,.docx" onChange={upload} />
      {loading ? "Analyzing..." : "📤 Upload PDF / DOCX / TXT"}
    </label>
  );
}
