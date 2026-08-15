import {
  Scale,
  Send,
  Loader2,
  MessageSquare,
} from "lucide-react";

import { useState } from "react";

import {
  askLegalQuestion,
} from "../services/api";

import SourceCard from "./SourceCard";


function ChatWindow() {

  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);


  const askQuestion = async () => {

    const text =
      question.trim();

    if (!text || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: text,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {

      const result =
        await askLegalQuestion(
          text,
          5
        );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          sources:
            result.sources || [],
        },
      ]);

    } catch (error) {

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error.message ||
            "Unable to process your question.",
          sources: [],
          error: true,
        },
      ]);

    } finally {

      setLoading(false);
    }
  };


  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();
    }
  };


  return (

    <section className="chat-card">

      <div className="section-title">

        <div className="section-icon">
          <MessageSquare size={18} />
        </div>

        <div>

          <h2>
            Legal Research Chat
          </h2>

          <p>
            Ask questions about your legal documents
          </p>

        </div>

      </div>


      <div className="chat-window">

        {messages.length === 0 ? (

          <div className="empty-chat">

            <div className="empty-icon">
              <Scale size={30} />
            </div>

            <h3>
              Start your legal research
            </h3>

            <p>
              Ask a question based on the
              available legal documents.
            </p>

            <button
              onClick={() =>
                setQuestion(
                  "What happens when a product is defective?"
                )
              }
            >
              What happens when a product is defective?
            </button>

            <button
              onClick={() =>
                setQuestion(
                  "What are the rights of a consumer?"
                )
              }
            >
              What are the rights of a consumer?
            </button>

          </div>

        ) : (

          <div className="messages">

            {messages.map(
              (message, index) => (

                <div
                  className={`message ${message.role}`}
                  key={index}
                >

                  <div className="message-avatar">

                    {message.role ===
                    "assistant" ? (
                      <Scale size={16} />
                    ) : (
                      "You"
                    )}

                  </div>


                  <div className="message-content">

                    <div className="message-name">

                      {message.role ===
                      "assistant"
                        ? "NyayAI"
                        : "You"}

                    </div>

                    <div className="message-text">

                      {message.content}

                    </div>


                    {message.sources?.length >
                      0 && (

                      <div className="sources">

                        <div className="sources-heading">
                          Sources
                        </div>

                        {message.sources.map(
                          (source, sourceIndex) => (

                            <SourceCard
                              key={sourceIndex}
                              source={source}
                            />

                          )
                        )}

                      </div>
                    )}

                  </div>

                </div>

              )
            )}


            {loading && (

              <div className="message assistant">

                <div className="message-avatar">
                  <Scale size={16} />
                </div>

                <div className="message-content">

                  <div className="message-name">
                    NyayAI
                  </div>

                  <div className="loading">

                    <Loader2
                      size={15}
                      className="spin"
                    />

                    Searching legal documents...

                  </div>

                </div>

              </div>

            )}

          </div>

        )}

      </div>


      <div className="chat-input">

        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(
              event.target.value
            )
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask a legal question..."
          disabled={loading}
        />

        <button
          className="send-button"
          onClick={askQuestion}
          disabled={
            loading ||
            !question.trim()
          }
        >

          {loading ? (
            <Loader2
              size={18}
              className="spin"
            />
          ) : (
            <Send size={18} />
          )}

        </button>

      </div>

    </section>
  );
}


export default ChatWindow;
