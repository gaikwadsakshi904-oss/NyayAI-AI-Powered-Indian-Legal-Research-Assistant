export default function SourceCard({ source }) {
  return (
    <div className="source-card">
      <strong>📚 {source.source}</strong>
      <small>Similarity: {source.score}</small>
      <p>{source.excerpt}</p>
    </div>
  );
}
