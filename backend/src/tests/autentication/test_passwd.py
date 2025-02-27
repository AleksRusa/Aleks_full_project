import pytest

from auth.utils import hash_password, validate_password

@pytest.mark.parametrize("password", ["password", "1234346432", "PIk21][;!]"])
def test_hash_password(password):
    hashed_password = hash_password(password)
    print(hashed_password)

    assert isinstance(hashed_password, bytes), "Хеш пароля должен быть типа bytes"
    assert len(hashed_password) > 0, "Хеш пароля не должен быть пустым"

@pytest.mark.parametrize("password", ["password", "1234346432", "PIk21][;!]"])
def test_verify_password(password):
    hashed_password = hash_password(password)

    assert validate_password(password, hashed_password)

@pytest.mark.parametrize("password", ["password", "1234346432", "PIk21][;!]"])
def test_verify_wrong_password(password):
    wrong_password = "wrongpas"
    hashed_password = hash_password(password)

    assert not validate_password(wrong_password, hashed_password)
