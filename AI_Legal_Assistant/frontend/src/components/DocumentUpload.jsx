import {
  Upload,
  FileText,
  X,
  Loader2,
  CheckCircle,
} from "lucide-react";

import { useRef, useState } from "react";

import { uploadDocument } from "../services/api";


function DocumentUpload() {

  const inputRef = useRef(null);

  const [files, setFiles] = useState([]);

  const [uploading, setUploading] =
    useState(false);

  const [message, setMessage] =
    useState("");


  const selectFiles = (event) => {

    const selected =
      Array.from(
        event.target.files || []
      );

    setFiles(selected);
    setMessage("");
  };


  const removeFile = (index) => {

    setFiles(
      files.filter(
        (_, i) => i !== index
      )
    );
  };


  const handleUpload = async () => {

    if (!files.length) {
      return;
    }

    setUploading(true);
    setMessage("");

    try {

      for (const file of files) {

        await uploadDocument(file);
      }

      setMessage(
        "Documents uploaded successfully."
      );

      setFiles([]);

    } catch (error) {

      setMessage(
        error.message ||
        "Upload failed."
      );

    } finally {

      setUploading(false);
    }
  };


  return (

    <section className="upload-card">

      <div className="section-title">

        <div className="section-icon">
          <Upload size={18} />
        </div>

        <div>

          <h2>
            Legal Knowledge Base
          </h2>

          <p>
            Upload PDF, DOCX or TXT documents
          </p>

        </div>

      </div>


      <input
        ref={inputRef}
        type="file"
        multiple
        accept=".pdf,.docx,.txt"
        hidden
        onChange={selectFiles}
      />


      <button
        className="drop-zone"
        onClick={() =>
          inputRef.current?.click()
        }
      >

        <div className="upload-circle">
          <Upload size={24} />
        </div>

        <strong>
          Select legal documents
        </strong>

        <span>
          PDF • DOCX • TXT
        </span>

      </button>


      {files.length > 0 && (

        <div className="selected-files">

          {files.map(
            (file, index) => (

              <div
                className="selected-file"
                key={`${file.name}-${index}`}
              >

                <FileText size={16} />

                <span>
                  {file.name}
                </span>

                <button
                  onClick={() =>
                    removeFile(index)
                  }
                >
                  <X size={15} />
                </button>

              </div>
            )
          )}

        </div>
      )}


      {files.length > 0 && (

        <button
          className="primary-button"
          onClick={handleUpload}
          disabled={uploading}
        >

          {uploading ? (
            <>
              <Loader2
                size={17}
                className="spin"
              />
              Uploading...
            </>
          ) : (
            <>
              <Upload size={17} />
              Upload Documents
            </>
          )}

        </button>
      )}


      {message && (

        <div className="upload-message">

          <CheckCircle size={16} />

          {message}

        </div>

      )}

    </section>
  );
}


export default DocumentUpload;
