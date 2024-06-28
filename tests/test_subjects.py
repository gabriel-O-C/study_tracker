

def test_create_subject(client):
    response = client.post("/api/v1/subjects/", json={
        'name': 'História'
    })

    assert response.json() == {
        'id': 1,
        'name': 'História',
    }
