from fastapi import FastAPI, HTTPException

app = FastAPI(title="Users Service")

USERS = {
    1: {"id": 1, "email": "alice@example.com"},
    2: {"id": 2, "email": "bob@example.com"},
}

@app.get("/users/{id}")
def get_user(id: int):
    user = USERS.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
