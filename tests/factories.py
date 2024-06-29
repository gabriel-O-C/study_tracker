from datetime import datetime

import factory
import factory.fuzzy

from src.subjects.models import Subject


class SubjectFactory(factory.Factory):
    class Meta:
        model = Subject

    name = factory.Sequence(lambda n: f'test-{n}')
    updated_at = datetime.now()
