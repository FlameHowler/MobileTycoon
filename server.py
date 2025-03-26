import sqlite3

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Инициализация базы данных SQLite
conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY, money INTEGER, phones TEXT)''')
conn.commit()

# Отдача статики (мини-аппа)
app.mount("/web", StaticFiles(directory="web"), name="web")

class UserAction(BaseModel):
    user_id: int
    action: str

@app.post("/api/action")
async def handle_action(data: UserAction):
    user_id = data.user_id
    action = data.action

    # Получаем данные пользователя из базы
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        # Если пользователя нет в базе, создаем нового
        cursor.execute("INSERT INTO users (user_id, money, phones) VALUES (?, ?, ?)", (user_id, 10000, "[]"))
        conn.commit()
        user = (user_id, 10000, "[]")

    phones = eval(user[2])  # Преобразуем строку с телефонами в список

    if action == "new_phone":
        phones.append("Новый смартфон")
        cursor.execute("UPDATE users SET phones = ? WHERE user_id = ?", (str(phones), user_id))
        conn.commit()
        return {"status": "ok", "message": "Смартфон добавлен!"}

    elif action == "stats":
        return {"status": "ok", "data": {"money": user[1], "phones": phones}}

    return {"status": "error", "message": "Неизвестное действие"}

@app.get("/")
async def serve_index():
    return FileResponse("web/index.html")