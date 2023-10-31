import pymongo
import psycopg2

# Підключення до MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]  # Замініть на вашу назву бази даних MongoDB
    return db

# Підключення до PostgreSQL
def connect_to_postgresql():
    conn = psycopg2.connect(
        database="Postgres",  # Замініть на вашу назву бази даних PostgreSQL
        user="vikkimrrr7",          # Замініть на ваше ім'я користувача PostgreSQL
        password="VikaVikaGo78",  # Замініть на ваш пароль PostgreSQL
        host="localhost",
        port="5432"
    )
    return conn

# Копіювання даних із MongoDB до PostgreSQL
def migrate_data():
    mongodb = connect_to_mongodb()
    postgresql = connect_to_postgresql()

    # Отримання даних з MongoDB (приклад для колекції "quotes")
    mongodb_data = mongodb["quotes"].find()

    # Запис даних у PostgreSQL
    cursor = postgresql.cursor()
    for data in mongodb_data:
        text = data["text"]
        author = data["author"]

        # Виконати INSERT запит у таблицю PostgreSQL (приклад для таблиці "myapp_quote")
        cursor.execute("INSERT INTO myapp_quote (text, author_id) VALUES (%s, %s)",
                       (text, author))

    # Закрити підключення та зберегти зміни
    postgresql.commit()
    cursor.close()

if __name__ == "__main__":
    migrate_data()