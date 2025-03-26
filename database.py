import sqlite3

class Database:
    def init(self, db_name="game.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def _execute_query(self, query, params=()):
        """Вспомогательная функция для выполнения SQL-запросов"""
        with self.conn:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()

    def create_tables(self):
        """Создаёт таблицы, если их нет"""
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                money INTEGER DEFAULT 10000
            )
        """)
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                cpu TEXT,
                ram TEXT,
                storage TEXT,
                battery TEXT,
                cost INTEGER,
                FOREIGN KEY(user_id) REFERENCES players(user_id)
            )
        """)

    def add_player(self, user_id):
        """Добавляет нового игрока"""
        self._execute_query("INSERT OR IGNORE INTO players (user_id) VALUES (?)", (user_id,))

    def get_money(self, user_id):
        """Возвращает баланс игрока"""
        result = self._execute_query("SELECT money FROM players WHERE user_id = ?", (user_id,))
        return result[0][0] if result else 10000  # Если пользователя нет, возвращаем стартовый баланс

    def update_money(self, user_id, amount):
        """Обновляет баланс игрока"""
        self._execute_query("UPDATE players SET money = ? WHERE user_id = ?", (amount, user_id))

    def add_phone(self, user_id, name, cpu, ram, storage, battery, cost):
        """Добавляет смартфон в базу"""
        self._execute_query("""
            INSERT INTO phones (user_id, name, cpu, ram, storage, battery, cost) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, cpu, ram, storage, battery, cost))

    def get_phones(self, user_id):
        """Возвращает список смартфонов игрока"""
        return self._execute_query("SELECT name, cpu, ram, storage, battery FROM phones WHERE user_id = ?", (user_id,))