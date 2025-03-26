from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Простая база данных (заменим на SQLite позже)
users = {}


class UserAction(BaseModel):
    user_id: int
    action: str


@app.post("/api/action")
async def handle_action(data: UserAction):
    user_id = data.user_id
    action = data.action

    if user_id not in users:
        users[user_id] = {"money": 10000, "phones": []}

    if action == "new_phone":
        users[user_id]["phones"].append("Новый смартфон")
        return {"status": "ok", "message": "Смартфон добавлен!"}

    elif action == "stats":
        return {"status": "ok", "data": users[user_id]}

    return {"status": "error", "message": "Неизвестное действие"}