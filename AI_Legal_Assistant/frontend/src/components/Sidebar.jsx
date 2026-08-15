export default function Sidebar({ page, setPage }) {
  const items = [
    ["dashboard", "🏠 Dashboard"],
    ["chat", "💬 Legal Chat"],
    ["analyzer", "📄 Document Analyzer"],
    ["sources", "📚 Sources"],
    ["about", "ℹ️ About"]
  ];

  return (
    <aside className="sidebar">
      {items.map(([key, label]) => (
        <button
          key={key}
          className={page === key ? "active" : ""}
          onClick={() => setPage(key)}
        >
          {label}
        </button>
      ))}
    </aside>
  );
}
