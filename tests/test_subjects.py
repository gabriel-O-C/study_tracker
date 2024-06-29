from http import HTTPStatus

from factories import SubjectFactory


def test_create_subject_success(client):
    response = client.post('/api/v1/subjects/', json={'name': 'História'})

    assert response.json() == {
        'id': 1,
        'name': 'História',
    }

    assert response.status_code == HTTPStatus.CREATED


def test_create_subject_with_invalid_data(client):
    response = client.post('/api/v1/subjects/', json={'name': 1})

    assert (
        response.json()['detail'][0]['msg'] == 'Input should be a valid string'
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_subject_without_required_fields(client):
    response = client.post('/api/v1/subjects/', json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == 'Field required'


def test_create_subject_that_already_exists(client, subject):
    response = client.post('/api/v1/subjects/', json={'name': 'Teste'})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Subject already exists'


def test_list_subjects(session, client):
    expected_subjects = 3
    session.bulk_save_objects(SubjectFactory.create_batch(3))

    response = client.get('/api/v1/subjects/')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['subjects']) == expected_subjects


def test_update_subject(client, subject):
    response = client.put(
        '/api/v1/subjects/1',
        json={
            'name': 'Física',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'Física'}


def test_update_not_found_subject(client, subject):
    response = client.put(
        '/api/v1/subjects/999',
        json={
            'name': 'Física',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Subject not found'


def test_delete_subject(client, subject):
    response = client.delete('/api/v1/subjects/1')

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_not_found_subject(client, subject):

    response = client.delete('/api/v1/subjects/999')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Subject not found'
