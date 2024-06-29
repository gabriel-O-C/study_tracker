from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str


class PublicSubjectSchema(BaseModel):
    id: int
    name: str


class SubjectList(BaseModel):
    subjects: list[PublicSubjectSchema]
