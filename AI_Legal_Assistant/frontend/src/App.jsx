import { useEffect, useState } from "react";

import ChatBox from "./components/ChatBox";
import FileUpload from "./components/FileUpload";

import { checkHealth } from "./services/api";

import "./App.css";


export default function App() {

    const [page, setPage] = useState("chat");
    const [backendOnline, setBackendOnline] = useState(false);

    useEffect(() => {

        checkHealth()
            .then(() => setBackendOnline(true))
            .catch(() => setBackendOnline(false));

    }, []);


    return (
        <div className="app">

            <div className="background-glow glow-one"></div>
            <div className="background-glow glow-two"></div>


            <header className="navbar">

                <div
                    className="brand"
                    onClick={() => setPage("chat")}
                >

                    <div className="brand-icon">
                        N
                    </div>

                    <div>
                        <strong>NyayAI</strong>
                        <span>Legal Intelligence</span>
                    </div>

                </div>


                <nav>

                    <button
                        className={
                            page === "chat"
                                ? "active"
                                : ""
                        }
                        onClick={() =>
                            setPage("chat")
                        }
                    >
                        AI Legal Chat
                    </button>

                    <button
                        className={
                            page === "upload"
                                ? "active"
                                : ""
                        }
                        onClick={() =>
                            setPage("upload")
                        }
                    >
                        Document Analyzer
                    </button>

                </nav>


                <div
                    className={
                        backendOnline
                            ? "status online"
                            : "status offline"
                    }
                >

                    <span></span>

                    {backendOnline
                        ? "System Online"
                        : "Backend Offline"}

                </div>

            </header>


            <main>

                {page === "chat" ? (
                    <ChatBox />
                ) : (
                    <FileUpload />
                )}

            </main>


            <footer>

                <span>
                    NyayAI • AI-powered Indian legal research
                </span>

                <span>
                    For research purposes only. Not legal advice.
                </span>

            </footer>

        </div>
    );
}