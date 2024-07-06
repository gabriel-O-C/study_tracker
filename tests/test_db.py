from datetime import datetime

from sqlalchemy import select

from src.subjects.models import Subject


def test_create_subject(session):
    new_subject = Subject(name='História', updated_at=datetime.now())
    session.add(new_subject)
    session.commit()

    subject = session.scalar(select(Subject).where(Subject.name == 'História'))

    assert subject.name == 'História'
