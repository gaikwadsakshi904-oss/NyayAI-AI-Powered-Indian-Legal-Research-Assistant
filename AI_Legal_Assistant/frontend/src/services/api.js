const API_URL = "http://127.0.0.1:8000";

export async function uploadDocument(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/api/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Document upload failed."
    );
  }

  return data;
}


export async function askLegalQuestion(
  question,
  top_k = 5
) {
  const response = await fetch(
    `${API_URL}/api/chat/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        top_k,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to get legal answer."
    );
  }

  return data;
}


export async function checkHealth() {
  const response = await fetch(
    `${API_URL}/health`
  );

  return response.ok;
}
