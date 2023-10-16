from mongoengine import connect, StringField, ListField, ReferenceField, DateTimeField
from django.db import models
from django.contrib.auth.models import User

connect('cluster0', host='mongodb+srv://vikkimrrr7:VikaVikaGo78@cluster0.kvolsxm.mongodb.net/')


import psycopg2

# Задайте параметри підключення
db_params = {
    'dbname': 'mydatabase',
    'user': 'vikkimrrr7',
    'password': 'VikaVikaGo78',
    'host': 'localhost',
    'port': '5432'  # Порт за замовчуванням для PostgreSQL
}

# Виконайте підключення
try:
    connection = psycopg2.connect(**db_params)
    print("Підключено до бази даних PostgreSQL")

    # Далі ви можете виконувати запити до бази даних
    # Наприклад, створення курсора та виконання SQL-запиту:
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"Версія PostgreSQL: {record[0]}")

except (Exception, psycopg2.Error) as error:
    print(f"Помилка підключення до бази даних: {error}")

finally:
    # Закрийте підключення
    if connection:
        cursor.close()
        connection.close()
        print("З'єднання закрито")


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:50]  # Виводимо перші 50 символів цитати

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Додайте інші поля користувача, які вам потрібні, наприклад, аватар, інформація про користувача тощо

