from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from ..config import LEGAL_DOCUMENTS_DIR
from ..document_analysis.ingest import ingest_documents
from ..embeddings.vector_store import build_vector_store


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # ======================================================
    # VALIDATE FILE
    # ======================================================

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )


    extension = Path(
        file.filename
    ).suffix.lower()


    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use PDF, DOCX or TXT."
            )
        )


    # ======================================================
    # CREATE DOCUMENT DIRECTORY
    # ======================================================

    LEGAL_DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # ======================================================
    # SAFE FILENAME
    # ======================================================

    safe_filename = Path(
        file.filename
    ).name


    destination = (
        LEGAL_DOCUMENTS_DIR /
        safe_filename
    )


    # ======================================================
    # SAVE FILE
    # ======================================================

    try:

        content = await file.read()

        destination.write_bytes(
            content
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to save document: {error}"
            )
        )


    # ======================================================
    # INGEST DOCUMENTS
    # ======================================================

    try:

        print("\n" + "=" * 60)
        print("NYAYAI DOCUMENT UPLOAD")
        print("=" * 60)

        print(
            f"Uploaded: {safe_filename}"
        )

        print(
            f"Size: {len(content):,} bytes"
        )


        print("\nStarting document ingestion...")

        chunks = ingest_documents()


        if not chunks:

            raise RuntimeError(
                "No text could be extracted "
                "from the uploaded document."
            )


        # ==================================================
        # BUILD / UPDATE FAISS
        # ==================================================

        print("\nUpdating FAISS vector database...")

        index = build_vector_store()


        print("\n" + "=" * 60)
        print("DOCUMENT PROCESSING COMPLETED")
        print("=" * 60)

        print(
            f"Total chunks: {len(chunks)}"
        )

        print(
            f"Total FAISS vectors: {index.ntotal}"
        )


    except Exception as error:

        print(
            f"\nDocument processing failed: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Document was uploaded but "
                f"processing failed: {error}"
            )
        )


    # ======================================================
    # RESPONSE
    # ======================================================

    return {

        "message":
            "Document uploaded and indexed successfully.",

        "filename":
            safe_filename,

        "size":
            len(content),

        "chunks":
            len(chunks),

        "vectors":
            index.ntotal,

        "status":
            "indexed",
    }
