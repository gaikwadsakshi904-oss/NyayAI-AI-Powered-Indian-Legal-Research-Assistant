from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


UPLOAD_DIR = (
    PROJECT_ROOT / "legal_documents"
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = (
        Path(file.filename)
        .suffix
        .lower()
    )

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, DOCX and TXT "
                "files are supported."
            )
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail=(
                "File is too large. "
                "Maximum size is 20 MB."
            )
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    safe_name = Path(
        file.filename
    ).name

    file_path = (
        UPLOAD_DIR / safe_name
    )

    file_path.write_bytes(
        content
    )

    return {

        "success": True,

        "filename": safe_name,

        "message":
            "Document uploaded successfully. "
            "Run ingestion to add it to the "
            "search index."

    }