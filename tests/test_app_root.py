from typing import Any


def test_root_ok(client: Any) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
