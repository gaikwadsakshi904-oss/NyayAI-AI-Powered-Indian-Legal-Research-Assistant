import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import LegalChat from "./pages/LegalChat";
import DocumentAnalyzer from "./pages/DocumentAnalyzer";
import Sources from "./pages/Sources";
import About from "./pages/About";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [page, setPage] = useState("dashboard");

  const renderPage = () => {
    if (page === "chat") return <LegalChat />;
    if (page === "analyzer") return <DocumentAnalyzer />;
    if (page === "sources") return <Sources />;
    if (page === "about") return <About />;
    return <Dashboard setPage={setPage} />;
  };

  return (
    <div className="app">
      <Navbar />
      <div className="layout">
        <Sidebar page={page} setPage={setPage} />
        <main className="content">{renderPage()}</main>
      </div>
    </div>
  );
}
