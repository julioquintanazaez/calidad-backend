from pydantic import BaseModel

class TextFileBase(BaseModel):
    name: str
    description: str | None = None

class TextFileCreate(TextFileBase):
    pass

class TextFile(TextFileBase):
    id: int
    file_path: str

    class Config:
        from_attributes = True
