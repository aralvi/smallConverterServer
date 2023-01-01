from fastapi import APIRouter, Form, UploadFile, HTTPException, status, Header
from app.services.document_service import DocumentService
from app.services.user_service import UserService
from app.schemas.document_schema import DocumentSchema, DocumentsResponse
from app.conversions.conversions import convert_file
from pydantic import BaseModel
import os
import io
import uuid
import aiofiles
from app.utils.jwt import decode_token
from typing import Optional
from app.utils.file_size import size
from app.utils.file_to_base64 import file_to_base64
from decouple import config
from datetime import datetime

document_router = APIRouter()

if (config("PLATFORM", cast=str) == "windows"):
    current_path = config("CURRENT_PATH", cast=str)+"docs\\"
else:
    current_path = config("CURRENT_PATH", cast=str)+"docs/"


@document_router.post("/upload", response_model=DocumentsResponse)
async def upload(file: UploadFile = Form(), token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    userId = str(user.id)
    # checking if the folder against the user is created or not
    if not os.path.exists(current_path+userId):
        os.makedirs(current_path+userId)
    # saving the file
    fileId = str(uuid.uuid4().hex)
    fileInfo = os.path.splitext(file.filename)
    fileName = fileInfo[0]
    fileType = fileInfo[1]
    # Now converting it into bytes
    file_bytes = file.file.read()
    file.file.close()
    async with aiofiles.open(f"{current_path+userId}/{fileId}{fileType}", "wb") as saved_file:
        await saved_file.write(file_bytes)
    saved_bytes_size = os.stat(
        f"{current_path+userId}/{fileId}{fileType}").st_size
    fileSize = size(saved_bytes_size)
    createdAt = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    doc_in = {
        "userId": userId,
        "fileId": fileId,
        "fileName": fileName,
        "fileType": fileType,
        "fileSize": fileSize,
        "createdAt": createdAt
    }
    doc = await DocumentService.create_document(doc_in)
    return {
        "message": "Successfully uploaded",
        "docs": doc
    }


class GetDocuments(BaseModel):
    docId: Optional[str] = None


@document_router.post("/get", response_model=DocumentsResponse)
async def get(data: GetDocuments, token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    userId = str(user.id)
    if (not data.docId):
        docs = await DocumentService.get_document_by_userId(userId)
    else:
        docs = await DocumentService.get_document_by_id(data.docId)

    return {
        "message": "Documents Successfully fetched",
        "docs": docs
    }


class DownloadDoc(BaseModel):
    docId: str


@document_router.post("/download")
async def download_file(data: DownloadDoc, token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    userId = str(user.id)
    # Getting document
    doc = await DocumentService.get_document_by_id(data.docId)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "No Document Found"
            }
        )
    fileId = doc["fileId"]
    fileName = doc["fileName"]
    fileType = doc["fileType"]
    b64 = file_to_base64(
        f"docs/{userId}/{fileId}{fileType}", remove_file=False)

    return {
        "message": "Documents Successfully fetched",
        "file": b64,
        "fileName": fileName+fileType
    }


@document_router.post("/getshared", response_model=DocumentsResponse)
async def download_file(data: DownloadDoc):
    # Getting document
    doc = await DocumentService.get_document_by_id(data.docId)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "No Document Found"
            }
        )

    return {
        "message": "Documents fetched",
        "docs": doc
    }


class DownloadShared(BaseModel):
    fileId: str
    fileType: str
    userId: str


@document_router.post("/downloadshared")
async def download_shared_file(data: DownloadShared):
    # Getting document
    b64 = file_to_base64(
        f"docs/{data.userId}/{data.fileId}{data.fileType}", remove_file=False)

    return {
        "message": "Documents fetched",
        "file": b64,
    }


class ConvertDoc(BaseModel):
    docId: str
    docName: str
    docType: str
    conversionType: str
    src: str
    tgt: str


@document_router.post("/convert")
async def convert_uploaded_file(data: ConvertDoc, token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    userId = str(user.id)
    # Getting document
    binary_file = open(
        f"docs/{userId}/{data.docId}{data.docType}", "rb")
    file = UploadFile(filename=data.docName+data.docType, file=binary_file)
    filename = data.docName+"."+data.tgt
    result = await convert_file(data.conversionType, file, {"src": data.src, "tgt": data.tgt})
    binary_file.close()
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
        "fileName": filename,
        "fileType": "type"
    }


class RenameDoc(BaseModel):
    id: str
    updateData: dict


@document_router.post("/update", response_model=DocumentsResponse)
async def update(data: RenameDoc, token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    doc = await DocumentService.update_document(data.id, data.updateData)
    return {
        "message": "document successfully updated",
        "docs": doc
    }


class DelDocument(BaseModel):
    id: str


@document_router.post("/delete")
async def delete(data: DelDocument, token: str | None = Header(default=None)):
    # Authenticating the user
    user = await UserService.authenticate(token)
    userId = str(user.id)
    doc = await DocumentService.delete_document(data.id)
    # Deleting file from storage
    if os.path.exists(f"{current_path+userId}/{doc.fileId}{doc.fileType}"):
        os.remove(f"{current_path+userId}/{doc.fileId}{doc.fileType}")
    return {
        "message": "document successfully deleted",
    }
