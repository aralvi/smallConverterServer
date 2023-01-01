from fastapi import File
from fastapi.responses import Response
from pydantic import BaseModel, Field


class ConversionResponse(BaseModel):
    message: str = Field(..., description="Response Message")
    file: str = Field(..., description="File in the form of base64 string")
    fileName: str = Field(..., description="Name of the file")
    fileType: str = Field(..., description="Mime type of the file")


class ConversionMeta(BaseModel):
    src: str = Field(..., description="Source file type")
    tgt: str = Field(..., description="Target file type")
