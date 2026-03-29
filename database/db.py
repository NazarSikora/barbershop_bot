import aiosqlite

DB_PATH = "barbershop.db"

async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблиця користувачів
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                name TEXT,
                phone TEXT
            )
        """)

        # Таблиця послуг
        await db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """)

        # Таблиця записів
        await db.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        """)

        await db.commit()


async def add_user(telegram_id: int, name: str, phone: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id, name, phone)
            VALUES (?, ?, ?)
        """, (telegram_id, name, phone))
        await db.commit()


async def get_services():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT id, name, price FROM services") as cursor:
            return await cursor.fetchall()


async def add_appointment(user_id: int, service_id: int, date: str, time: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO appointments (user_id, service_id, date, time)
            VALUES (?, ?, ?, ?)
        """, (user_id, service_id, date, time))
        await db.commit()