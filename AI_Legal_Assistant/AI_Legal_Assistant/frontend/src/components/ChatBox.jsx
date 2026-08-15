import { useState } from "react";
import { askQuestion } from "../services/api";
import SourceCard from "./SourceCard";
import Loading from "./Loading";

export default function ChatBox() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const q = question.trim();
    setMessages(m => [...m, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const data = await askQuestion(q);
      setMessages(m => [...m, {
        role: "assistant",
        text: data.answer,
        sources: data.sources || []
      }]);
    } catch (err) {
      setMessages(m => [...m, {
        role: "assistant",
        text: err.response?.data?.detail || "Unable to connect to the backend."
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <div className="messages">
        {messages.length === 0 && (
          <div className="empty">
            <h2>Ask a legal question</h2>
            <p>Example: What are my basic consumer rights?</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <p>{m.text}</p>
            {m.sources?.map((s, j) => <SourceCard key={j} source={s} />)}
          </div>
        ))}
        {loading && <Loading />}
      </div>

      <form className="chat-form" onSubmit={submit}>
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Type your legal question..."
        />
        <button>Ask</button>
      </form>
    </div>
  );
}
