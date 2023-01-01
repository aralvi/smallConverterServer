from fastapi import APIRouter, Form, UploadFile, HTTPException, status
from app.conversions.conversions import convert_file
from app.schemas.conversion_schema import ConversionResponse
import json


conversion_router = APIRouter()


@conversion_router.post("/", response_model=ConversionResponse)
async def convert(conversionType: str = Form(), file: UploadFile = Form(), meta: str = Form()):
    meta = json.loads(meta)
    result = await convert_file(conversionType, file, meta)
    file.file.close()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Requested Conversion is Not supported"
            }
        )
    return {
        "message": "successfully converted",
        "file": result["file"],
        "fileName": result["filename"],
        "fileType": result["filetype"]
    }
