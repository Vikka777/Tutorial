import psycopg2
from pymongo import MongoClient

def migrate_data():
    # Підключення до MongoDB
    mongo_client = MongoClient('mongodb://localhost:27017')
    mongo_db = mongo_client['MobgoDB']

    # Отримання колекції з даними (наприклад, "цитати")
    collection = mongo_db['цитати']

    # Отримання всіх документів із колекції
    documents = collection.find()

    # Збереження даних у вигляді списку словників
    data_to_migrate = list(documents)

    # Підключення до PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="Postgres",
        user="vikkimrrr7",
        password="VikaVikaGo78"
    )

    # Створення курсора
    cur = conn.cursor()

    # Створення таблиці користувачів
    cur.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        );
    """)

    # Імпорт даних в таблицю користувачів
    for row in data_to_migrate:
        cur.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s);
        """, (row['name'], row['email'], row['password']))

    # Збереження змін
    conn.commit()

    # Закриття підключень
    conn.close()
    mongo_client.close()

# Виклик функції для міграції даних
migrate_data()
