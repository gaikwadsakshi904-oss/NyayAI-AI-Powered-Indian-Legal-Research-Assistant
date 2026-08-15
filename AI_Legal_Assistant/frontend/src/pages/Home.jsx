import {
  ShieldCheck,
  BookOpen,
  Scale,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/Navbar";
import DocumentUpload from "../components/DocumentUpload";
import ChatWindow from "../components/ChatWindow";


function Home() {

  return (

    <div className="app">

      <Navbar />

      <main className="main">

        <section className="hero">

          <div className="hero-badge">

            <Sparkles size={14} />

            AI-Powered Indian Legal Research

          </div>


          <h1>
            Understand Indian Law
            <span>
              with confidence.
            </span>
          </h1>


          <p>
            Upload legal documents, ask questions,
            and retrieve relevant legal information
            with transparent source attribution.
          </p>

        </section>


        <DocumentUpload />

        <ChatWindow />


        <section className="trust-bar">

          <div>
            <ShieldCheck size={18} />
            Source-grounded
          </div>

          <div>
            <BookOpen size={18} />
            Document-based
          </div>

          <div>
            <Scale size={18} />
            Indian Legal Context
          </div>

        </section>


        <footer className="disclaimer">

          <ShieldCheck size={15} />

          NyayAI provides AI-assisted legal
          information for research and educational
          purposes only. It does not constitute
          professional legal advice.

        </footer>

      </main>

    </div>
  );
}


export default Home;
