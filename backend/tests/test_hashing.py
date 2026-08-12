from security.hashing import hash_password, verify_password


def test_hash_password_returns_different_string_than_plain():
    password = 'password'
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed != password


def test_hash_password_is_salted():
    password = 'password'
    hashed_one = hash_password(password)
    hashed_two = hash_password(password)

    assert hashed_one != hashed_two


def test_verify_password_with_correct_password():
    password = 'password'
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_with_incorrect_password():
    hashed = hash_password('password')

    assert verify_password('wrong_password', hashed) is False
