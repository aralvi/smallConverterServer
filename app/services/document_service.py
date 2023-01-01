from fastapi import HTTPException, status
from app.schemas.document_schema import DocumentSchema
from app.models.document_model import Document


class DocumentService:
    @staticmethod
    async def create_document(document: DocumentSchema):
        try:
            doc_in = Document(
                userId=document["userId"],
                fileId=document["fileId"],
                fileName=document["fileName"],
                fileType=document["fileType"],
                fileSize=document["fileSize"],
                createdAt=document["createdAt"]
            )
            doc = await doc_in.save()
            return doc
        except Exception as error:
            return error

    @staticmethod
    async def get_document_by_userId(userId: str):
        try:
            # docs = await Document.find({"userId": userId})
            docs = await Document.find_many({"userId": userId}).to_list()
            return docs
        except Exception as error:
            return error

    @staticmethod
    async def get_document_by_id(id: str):
        try:
            doc = await Document.find_one({"fileId": id})
            return dict(doc)
        except Exception as error:
            return error

    @staticmethod
    async def update_document(id: str, updateData):
        try:
            doc = await Document.find_one({"fileId": id})
            await doc.update({"$set": updateData})
            return dict(doc)
        except Exception as error:
            return error

    @staticmethod
    async def delete_document(id: str):
        try:
            doc = await Document.find_one({"fileId": id})
            docCopy = doc
            await doc.delete()
            return docCopy
        except Exception as error:
            return error
