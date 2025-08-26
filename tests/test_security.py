from app.core.security import hash_password, make_token, parse_token, verify_password


def test_token_roundtrip() -> None:
    uid = 123
    token = make_token(uid, expires_minutes=5)
    assert isinstance(token, str) and token
    parsed = parse_token(token)
    assert parsed == uid


def test_password_hash_and_verify() -> None:
    pw = "s3cret!"
    hpw = hash_password(pw)
    assert hpw and hpw != pw
    assert verify_password(pw, hpw)
    assert not verify_password("wrong", hpw)
