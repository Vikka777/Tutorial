import psycopg2
from pymongo import MongoClient

def migrate_data():
    mongo_client = MongoClient('mongodb://localhost:27017')
    mongo_db = mongo_client['MobgoDB']

    collection = mongo_db['цитати']

    documents = collection.find()

    data_to_migrate = list(documents)

    conn = psycopg2.connect(
        host="localhost",
        database="Postgres",
        user="vikkimrrr7",
        password="VikaVikaGo78"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        );
    """)

    for row in data_to_migrate:
        cur.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s);
        """, (row['name'], row['email'], row['password']))

    conn.commit()

    conn.close()
    mongo_client.close()

migrate_data()
