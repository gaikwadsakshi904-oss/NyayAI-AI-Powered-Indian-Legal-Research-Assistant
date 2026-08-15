import { useRef, useState } from "react";
import { analyzeDocument } from "../services/api";

export default function FileUpload() {
    const inputRef = useRef(null);

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    function handleFile(e) {
        const selected = e.target.files?.[0];

        if (!selected) return;

        const extension = selected.name
            .toLowerCase()
            .split(".")
            .pop();

        if (!["pdf", "docx", "txt"].includes(extension)) {
            setError("Only PDF, DOCX and TXT files are supported.");
            return;
        }

        setFile(selected);
        setMessage("");
        setError("");
    }

    async function upload() {
        if (!file) {
            setError("Please select a document first.");
            return;
        }

        setLoading(true);
        setMessage("");
        setError("");

        try {
            const result = await analyzeDocument(file);

            setMessage(
                `${result.filename} uploaded successfully.`
            );
        } catch (err) {
            setError(
                err.message || "Document upload failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <section className="upload-section">

            <div className="section-heading">
                <span className="eyebrow">
                    DOCUMENT ANALYZER
                </span>

                <h1>
                    Upload your
                    <span> legal document.</span>
                </h1>

                <p>
                    Upload PDF, DOCX or TXT documents.
                </p>
            </div>

            <div
                className="drop-zone"
                onClick={() => inputRef.current?.click()}
            >
                <div className="upload-icon">
                    ↑
                </div>

                <h2>
                    Upload a legal document
                </h2>

                <p>
                    Click here to browse your computer
                </p>

                <span className="file-types">
                    PDF • DOCX • TXT
                </span>

                <input
                    ref={inputRef}
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFile}
                    hidden
                />
            </div>

            {file && (
                <div className="selected-file">
                    <div>
                        <strong>
                            📄 {file.name}
                        </strong>

                        <span>
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                        </span>
                    </div>

                    <button
                        onClick={upload}
                        disabled={loading}
                    >
                        {loading
                            ? "Uploading..."
                            : "Upload Document"}
                    </button>
                </div>
            )}

            {message && (
                <div className="success-card">
                    ✓ {message}
                </div>
            )}

            {error && (
                <div className="error-card">
                    <strong>Upload failed</strong>
                    <p>{error}</p>
                </div>
            )}

        </section>
    );
}
