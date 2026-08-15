import { useState } from "react";
import { askQuestion } from "../services/api";

export default function ChatBox() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();

        if (!question.trim()) return;

        setLoading(true);
        setError("");
        setAnswer("");
        setSources([]);

        try {
            const result = await askQuestion(question, 5);

            setAnswer(result.answer || "No answer returned.");
            setSources(result.sources || []);
        } catch (err) {
            setError(err.message || "Unable to contact NyayAI.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <section className="chat-section">

            <div className="section-heading">
                <span className="eyebrow">LEGAL AI ASSISTANT</span>

                <h1>
                    Ask anything about
                    <span> Indian Law.</span>
                </h1>

                <p>
                    Get AI-powered answers grounded in
                    your legal knowledge base.
                </p>
            </div>

            <form
                className="question-box"
                onSubmit={handleSubmit}
            >
                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Example: What happens when a product is defective?"
                    rows={5}
                    disabled={loading}
                />

                <div className="question-footer">
                    <span>
                        Ask a legal research question
                    </span>

                    <button
                        type="submit"
                        disabled={loading || !question.trim()}
                    >
                        {loading ? "Researching..." : "Ask NyayAI →"}
                    </button>
                </div>
            </form>

            {loading && (
                <div className="loading-card">
                    <div className="loader"></div>

                    <div>
                        <strong>
                            Researching legal sources...
                        </strong>

                        <p>
                            Searching the NyayAI knowledge base.
                        </p>
                    </div>
                </div>
            )}

            {error && (
                <div className="error-card">
                    <strong>Something went wrong</strong>
                    <p>{error}</p>
                </div>
            )}

            {answer && !loading && (
                <div className="answer-card">

                    <div className="answer-header">
                        <div>
                            <span className="eyebrow">
                                NYAYAI RESPONSE
                            </span>

                            <h2>Legal Analysis</h2>
                        </div>

                        <div className="ai-badge">
                            AI
                        </div>
                    </div>

                    <div className="answer-content">
                        {answer}
                    </div>

                    {sources.length > 0 && (
                        <div className="sources">
                            <h3>📚 Sources</h3>

                            {sources.map((source, index) => (
                                <div
                                    className="source-card"
                                    key={index}
                                >
                                    <div>
                                        <strong>
                                            {source.document}
                                        </strong>

                                        <span>
                                            Legal document
                                        </span>
                                    </div>

                                    <div className="score">
                                        {(
                                            Number(source.score || 0) * 100
                                        ).toFixed(1)}%
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                </div>
            )}
        </section>
    );
}
