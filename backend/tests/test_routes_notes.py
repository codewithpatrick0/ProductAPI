from security.tokens import create_access_token


def test_create_note_success(authenticated_client):
    response = authenticated_client.post('/notes/', json={
        'title': 'Hello World',
        'content': 'Test Content'
    })

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Hello World'
    assert data['content'] == 'Test Content'


def test_create_note_without_auth(client):
    response = client.post('/notes/', json={
        'title': 'Hello World',
        'content': 'Test Content'
    })

    assert response.status_code == 401


def test_list_notes_only_returns_own_notes(authenticated_client):
    authenticated_client.post('/notes/', json={'title': 'Note 1', 'content': 'Content 1'})
    authenticated_client.post('/notes/', json={'title': 'Note 2', 'content': 'Content 2'})

    response = authenticated_client.get('/notes/')

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_note_success(authenticated_client):
    create_response = authenticated_client.post('/notes/', json={'title': 'Hello', 'content': 'World'})
    note_id = create_response.json()['id']

    response = authenticated_client.get(f'/notes/{note_id}')

    assert response.status_code == 200
    assert response.json()['id'] == note_id


def test_get_note_not_found(authenticated_client):
    response = authenticated_client.get('/notes/9999')

    assert response.status_code == 404


def test_get_note_wrong_owner(authenticated_client, second_registered_user):
    create_response = authenticated_client.post('/notes/', json={'title': 'Hello', 'content': 'World'})
    note_id = create_response.json()['id']

    authenticated_client.cookies.set('access_token', create_access_token(second_registered_user.user.id))

    response = authenticated_client.get(f'/notes/{note_id}')

    assert response.status_code == 404


def test_edit_note_success(authenticated_client):
    create_response = authenticated_client.post('/notes/', json={'title': 'Old Title', 'content': 'Old Content'})
    note_id = create_response.json()['id']

    response = authenticated_client.patch(f'/notes/{note_id}', json={'title': 'New Title'})

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'New Title'
    assert data['content'] == 'Old Content'


def test_edit_note_wrong_owner(authenticated_client, second_registered_user):
    create_response = authenticated_client.post('/notes/', json={'title': 'Old Title', 'content': 'Old Content'})
    note_id = create_response.json()['id']

    authenticated_client.cookies.set('access_token', create_access_token(second_registered_user.user.id))

    response = authenticated_client.patch(f'/notes/{note_id}', json={'title': 'Hacked'})

    assert response.status_code == 404


def test_delete_note_success(authenticated_client):
    create_response = authenticated_client.post('/notes/', json={'title': 'Bye', 'content': 'Bye Content'})
    note_id = create_response.json()['id']

    response = authenticated_client.delete(f'/notes/{note_id}')
    assert response.status_code == 204

    get_response = authenticated_client.get(f'/notes/{note_id}')
    assert get_response.status_code == 404


def test_delete_note_wrong_owner(authenticated_client, second_registered_user):
    create_response = authenticated_client.post('/notes/', json={'title': 'Bye', 'content': 'Bye Content'})
    note_id = create_response.json()['id']

    authenticated_client.cookies.set('access_token', create_access_token(second_registered_user.user.id))

    response = authenticated_client.delete(f'/notes/{note_id}')
    assert response.status_code == 404
