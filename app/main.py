from fastapi import FastAPI

app = FastAPI(title="Discovery Bot")


@app.get("/")
def root() -> dict[str, bool]:
    return {"ok": True}
