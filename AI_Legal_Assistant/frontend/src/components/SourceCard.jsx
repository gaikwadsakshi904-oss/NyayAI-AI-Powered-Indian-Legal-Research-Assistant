import {
  FileText,
  ExternalLink,
} from "lucide-react";


function SourceCard({ source }) {

  return (
    <div className="source-card">

      <FileText
        size={16}
        className="source-icon"
      />

      <div className="source-info">

        <strong>
          {source.document}
        </strong>

        <span>
          Relevance:{" "}
          {source.score
            ? `${(
                source.score * 100
              ).toFixed(1)}%`
            : "N/A"}
        </span>

      </div>

      <ExternalLink size={14} />

    </div>
  );
}


export default SourceCard;
