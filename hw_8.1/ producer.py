import pika
import json
from faker import Faker
from models import Contact

fake = Faker()

# Зчитуємо конфігурацію з JSON-файлу
with open('producer.json', 'r') as config_file:
    config = json.load(config_file)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config['rabbitmq']['host'],
    port=config['rabbitmq']['port']
))
channel = connection.channel()

# Створення черги для надсилання ідентифікаторів контактів
channel.queue_declare(queue=config['rabbitmq']['queue_name'])

# Генерування фейкових контактів і збереження їх у базі даних
for _ in range(10):  # Генеруємо 10 контактів для прикладу
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    # Надсилаємо ідентифікатор контакту в чергу RabbitMQ
    message = {
        'contact_id': str(contact.id) # type: ignore
    }
    channel.basic_publish(exchange='', routing_key=config['rabbitmq']['queue_name'], body=json.dumps(message))

print("Генерація контактів та відправка ідентифікаторів завершена")

# Закриваємо з'єднання
connection.close()
