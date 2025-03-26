from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mobile Tycoon</title>
    </head>
    <body>
        <h1>Добро пожаловать в Mobile Tycoon!</h1>
        <p>Скоро здесь будет игра...</p>
    </body>
    </html>
    """

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


#mini app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Раздаём файлы из папки "web"
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
async def serve_index():
    return FileResponse("web/index.html")