from beanie import Document


class Document(Document):
    userId: str
    fileId: str
    fileName: str
    fileType: str
    fileSize: str
    createdAt: str

    class Settings:
        name = "documents"
