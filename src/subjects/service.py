from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from src.database import T_Session

from .models import Subject
from .schemas import SubjectSchema


class SubjectService:
    def post(session: T_Session, subject: SubjectSchema):
        db_subject = session.scalar(
            select(Subject).where(Subject.name == subject.name)
        )

        if db_subject:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Subject already exists',
            )

        db_subject = Subject(subject.name, updated_at=datetime.now())

        return db_subject

    def put(session: T_Session, subject: SubjectSchema, subject_id: int):
        db_subject: Subject = session.scalar(
            select(Subject).where(Subject.id == subject_id)
        )

        if not db_subject:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Subject not found'
            )

        db_subject.name = subject.name
        db_subject.updated_at = datetime.now()

        return db_subject

    def delete(session: T_Session, subject_id: int):
        db_subject = session.scalar(
            select(Subject).where(Subject.id == subject_id)
        )

        if not db_subject:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Subject not found'
            )

        return db_subject
