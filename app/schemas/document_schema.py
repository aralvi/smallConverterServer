from pydantic import BaseModel, Field


class DocumentSchema(BaseModel):

    userId: str = Field(..., description="User Id")
    fileName: str = Field(..., description="File name")
    fileType: str = Field(..., description="File Type")
    fileSize: str = Field(..., description="File Size")
    fileId: str = Field(..., description="File Id")
    createdAt: str = Field(..., description="Created At")


class DocumentsResponse(BaseModel):
    message: str
    docs: list | dict
