const API_URL = "http://127.0.0.1:8000";

async function readError(response) {
    try {
        const data = await response.json();

        if (typeof data.detail === "string") {
            return data.detail;
        }

        return JSON.stringify(data.detail || data);
    } catch {
        return `Request failed with status ${response.status}`;
    }
}

export async function checkHealth() {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
        throw new Error("Backend is not healthy.");
    }

    return response.json();
}

export async function askQuestion(question, top_k = 5) {
    const response = await fetch(`${API_URL}/api/chat/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question: question.trim(),
            top_k,
        }),
    });

    if (!response.ok) {
        throw new Error(await readError(response));
    }

    return response.json();
}

export async function analyzeDocument(file) {
    if (!file) {
        throw new Error("Please select a document.");
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/api/documents/upload`,
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        throw new Error(await readError(response));
    }

    return response.json();
}