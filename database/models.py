import sqlite3
from faker import Faker
import random
from datetime import date
import os
import glob

# Підключення до бази даних
conn = sqlite3.connect('mydatabase.db')

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor()
# Отримання списку SQL-файлів у папці "sql_queries"
sql_files = glob.glob("sql_queries/*.sql")

# Виконання всіх SQL-запитів
for sql_file in sql_files:
    with open(sql_file, 'r') as file:
        sql_query = file.read()
        cursor.execute(sql_query)
        result = cursor.fetchall()

# Створення таблиць
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        group_id INT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id SERIAL PRIMARY KEY,
        group_name VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id SERIAL PRIMARY KEY,
        subject_name VARCHAR(50),
        teacher_id INT
    )
''')

cursor.execute('''
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
    cursor.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))

# Генерація викладачів
for _ in range(5):
    first_name = faker.first_name()
    last_name = faker.last_name()
    cursor.execute("INSERT INTO teachers (first_name, last_name) VALUES (?, ?)", (first_name, last_name))

# Генерація предметів із призначенням викладачів
subjects = ["Math", "Science", "History", "English", "Programming"]
for subject in subjects:
    teacher_id = random.randint(1, 5)  # 5 викладачів
    cursor.execute("INSERT INTO subjects (subject_name, teacher_id) VALUES (?, ?)", (subject, teacher_id))

# Генерація студентів та оцінок
for _ in range(50):
    first_name = faker.first_name()
    last_name = faker.last_name()
    group_id = random.randint(1, 3)  # 3 групи
    cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES (?, ?, ?)", (first_name, last_name, group_id))

    student_id = cursor.lastrowid  # Отримуємо ID студента, щойно вставленого в базу даних

    for subject_id in range(1, 6):
        grade = round(random.uniform(2.0, 5.0), 2)
        date_received = faker.date_between(start_date=date(2022, 1, 1), end_date=date(2023, 1, 1))
        cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)", (student_id, subject_id, grade, date_received))

# Закриття курсора
cursor.close()

# З'єднання з базою даних
conn.close()
