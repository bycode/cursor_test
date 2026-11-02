from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.detect.factory import get_detector
from app.services.verify import VerifyError, VerifyService

router = APIRouter(prefix="/api/v1", tags=["verify"])


@router.post("/verify")
async def verify_image(
    file: UploadFile = File(...),
    bbox: str = Form(...),
    db: Session = Depends(get_db),
) -> dict:
    if file.filename is None:
        raise HTTPException(status_code=400, detail="missing image filename")
    image_bytes = await file.read()
    service = VerifyService(db, get_detector())
    try:
        return service.run(
            image_bytes=image_bytes,
            filename=file.filename,
            bbox_raw=bbox,
            source="api",
        )
    except VerifyError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
