from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str


class PublicSubjectSchema(BaseModel):
    id: int
    name: str
