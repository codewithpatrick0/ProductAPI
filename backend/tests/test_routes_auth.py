def test_register_success(client):
    response = client.post('/auth/register', json={
        'name': 'Patrick',
        'username': 'Pat23',
        'password': 'password'
    })

    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'Pat23'
    assert 'password' not in data
    assert 'hash_password' not in data


def test_register_duplicate_username(client, registered_user):
    response = client.post('/auth/register', json={
        'name': 'Jorge',
        'username': registered_user.username,
        'password': '123456'
    })

    assert response.status_code == 409


def test_register_password_too_short(client):
    response = client.post('/auth/register', json={
        'name': 'Patrick',
        'username': 'Pat23',
        'password': '123'
    })

    assert response.status_code == 422


def test_login_success(client, registered_user):
    response = client.post('/auth/login', json={
        'username': registered_user.username,
        'password': registered_user.password
    })

    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'access_token' in response.cookies
    assert 'refresh_token' in response.cookies


def test_login_wrong_password(client, registered_user):
    response = client.post('/auth/login', json={
        'username': registered_user.username,
        'password': 'wrong_password'
    })

    assert response.status_code == 401


def test_login_username_not_found(client):
    response = client.post('/auth/login', json={
        'username': 'ghost',
        'password': 'whatever'
    })

    assert response.status_code == 401


def test_refresh_success(client, registered_user):
    login_response = client.post('/auth/login', json={
        'username': registered_user.username,
        'password': registered_user.password
    })
    assert login_response.status_code == 200

    refresh_response = client.post('/auth/refresh')

    assert refresh_response.status_code == 200
    assert 'access_token' in refresh_response.json()
    assert 'access_token' in refresh_response.cookies


def test_refresh_without_cookie(client):
    response = client.post('/auth/refresh')

    assert response.status_code == 401


def test_refresh_with_invalid_token(client):
    client.cookies.set('refresh_token', 'this.is.not.jwt')

    response = client.post('/auth/refresh')

    assert response.status_code == 401
