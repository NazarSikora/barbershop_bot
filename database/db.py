import aiosqlite

DB_PATH = "barbershop.db"

WORK_HOURS = [
    "10:00", "11:00", "12:00", "13:00",
    "14:00", "15:00", "16:00", "17:00", "18:00"
]

async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                name TEXT,
                phone TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS masters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                master_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (master_id) REFERENCES masters(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        """)

        await db.commit()
        await seed_data(db)


async def seed_data(db):
    async with db.execute("SELECT COUNT(*) FROM masters") as cursor:
        count = await cursor.fetchone()

    if count[0] == 0:
        await db.executemany(
            "INSERT INTO masters (name, specialization) VALUES (?, ?)",
            [
                ("✂️ Олексій", "Майстер по стрижках"),
                ("🪒 Михайло", "Майстер по голінню"),
                ("✂️🪒 Дмитро", "Універсальний майстер"),
            ]
        )

    async with db.execute("SELECT COUNT(*) FROM services") as cursor:
        count = await cursor.fetchone()

    if count[0] == 0:
        await db.executemany(
            "INSERT INTO services (name, price) VALUES (?, ?)",
            [
                ("Стрижка", 250),
                ("Гоління", 150),
                ("Комплекс", 350),
            ]
        )

    await db.commit()


async def add_user(telegram_id: int, name: str, phone: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id, name, phone)
            VALUES (?, ?, ?)
        """, (telegram_id, name, phone))
        await db.commit()


async def get_masters():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, name, specialization FROM masters"
        ) as cursor:
            return await cursor.fetchall()


async def get_services():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, name, price FROM services"
        ) as cursor:
            return await cursor.fetchall()


async def get_available_slots(master_id: int, date: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT time FROM appointments
            WHERE master_id = ? AND date = ?
        """, (master_id, date)) as cursor:
            booked = await cursor.fetchall()

    booked_times = [row[0] for row in booked]

    available = [slot for slot in WORK_HOURS if slot not in booked_times]
    return available


async def add_appointment(
    user_id: int,
    master_id: int,
    service_id: int,
    date: str,
    time: str
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO appointments (user_id, master_id, service_id, date, time)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, master_id, service_id, date, time))
        await db.commit()