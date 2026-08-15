import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export async function askQuestion(question) {
  const { data } = await api.post("/api/chat", { question });
  return data;
}

export async function analyzeDocument(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/api/analyze", form);
  return data;
}
