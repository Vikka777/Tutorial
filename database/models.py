import psycopg2
from faker import Faker
import random
from datetime import date

# З'єднання з базою даних PostgreSQL
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="localhost"
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Створення таблиць
cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        group_id INT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id SERIAL PRIMARY KEY,
        group_name VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id SERIAL PRIMARY KEY,
        subject_name VARCHAR(50),
        teacher_id INT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        grade_id SERIAL PRIMARY KEY,
        student_id INT,
        subject_id INT,
        grade DECIMAL(3, 2),
        date_received DATE
    )
''')

# Збереження змін у базі даних
conn.commit()

# Створення об'єкту Faker для генерації випадкових даних
faker = Faker()

# Генерація груп
groups = ["Group A", "Group B", "Group C"]
for group_name in groups:
    cur.execute("INSERT INTO groups (group_name) VALUES (%s)", (group_name,))

# Генерація викладачів
for _ in range(5):
    first_name = faker.first_name()
    last_name = faker.last_name()
    cur.execute("INSERT INTO teachers (first_name, last_name) VALUES (%s, %s)", (first_name, last_name))

# Генерація предметів із призначенням викладачів
subjects = ["Math", "Science", "History", "English", "Programming"]
for subject in subjects:
    teacher_id = random.randint(1, 5)  # 5 викладачів
    cur.execute("INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s)", (subject, teacher_id))

# Генерація студентів та оцінок
for _ in range(50):
    first_name = faker.first_name()
    last_name = faker.last_name()
    group_id = random.randint(1, 3)  # 3 групи
    cur.execute("INSERT INTO students (first_name, last_name, group_id) VALUES (%s, %s, %s)", (first_name, last_name, group_id))

    student_id = cur.lastrowid  # Отримуємо ID студента, щойно вставленого в базу даних

    for subject_id in range(1, 6):
        grade = round(random.uniform(2.0, 5.0), 2)
        date_received = faker.date_between(start_date=date(2022, 1, 1), end_date=date(2023, 1, 1))
        cur.execute("INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (%s, %s, %s, %s)", (student_id, subject_id, grade, date_received))

# Збереження змін у базі даних
conn.commit()

# Закриття з'єднання з базою даних
conn.close()
