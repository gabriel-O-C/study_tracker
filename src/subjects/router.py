from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.database import T_Session

from .models import Subject
from .schemas import PublicSubjectSchema, SubjectList, SubjectSchema
from .service import create_subject as service_create_subject

router = APIRouter(prefix='/api/v1/subjects', tags=['subjects'])


@router.post(
    '/', response_model=PublicSubjectSchema, status_code=HTTPStatus.CREATED
)
def create_subject(
    subject: SubjectSchema,
    session: T_Session,
):
    db_subject = service_create_subject(session, subject)
    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)

    return db_subject


@router.get('/', response_model=SubjectList, status_code=HTTPStatus.OK)
def list_subjects(session: T_Session):
    subjects = session.scalars(select(Subject)).all()

    return {'subjects': subjects}


@router.put(
    '/{subject_id}',
    response_model=PublicSubjectSchema,
    status_code=HTTPStatus.OK,
)
def update_subject(
    subject_id: int,
    subject: SubjectSchema,
    session: T_Session,
):
    db_subject: Subject = session.scalar(
        select(Subject).where(Subject.id == subject_id)
    )

    if not db_subject:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Subject not found'
        )

    db_subject.name = subject.name
    db_subject.updated_at = datetime.now()

    session.commit()
    session.refresh(db_subject)

    return db_subject


@router.delete('/{subject_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_subject(subject_id: int, session: T_Session):  # type: ignore
    db_subject = session.scalar(
        select(Subject).where(Subject.id == subject_id)
    )

    if not db_subject:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Subject not found'
        )

    session.delete(db_subject)
    session.commit()
