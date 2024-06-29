from pydantic import BaseModel, ConfigDict


class SubjectSchema(BaseModel):
    name: str


class PublicSubjectSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class SubjectList(BaseModel):
    subjects: list[PublicSubjectSchema]
