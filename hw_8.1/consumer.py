import pika
import json
from models import Contact

# Зчитуємо конфігурацію з JSON-файлу
with open('consumer.json', 'r') as config_file:
    config = json.load(config_file)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config['rabbitmq']['host'],
    port=config['rabbitmq']['port']
))
channel = connection.channel()

# Створення черги для отримання ідентифікаторів контактів
channel.queue_declare(queue=config['rabbitmq']['queue_name'])

def send_email(contact_id):
    # Функція-заглушка для надсилання email (імітація)
    print(f"Відправка email до контакту з ID {contact_id}")
    # Додайте реальний код для надсилання email тут

    # Позначаємо, що email був відправлений
    contact = Contact.objects.get(id=contact_id) # type: ignore
    contact.sent_email = True
    contact.save()

def callback(ch, method, properties, body):
    # Отримуємо ідентифікатор контакту з повідомлення
    message = json.loads(body)
    contact_id = message['contact_id']

    # Викликаємо функцію для надсилання email
    send_email(contact_id)
    print(f"Оброблено повідомлення для контакту з ID {contact_id}")

# Підписуємось на чергу для отримання повідомлень
channel.basic_consume(queue=config['rabbitmq']['queue_name'], on_message_callback=callback, auto_ack=True)

print("Чекаємо на повідомлення з RabbitMQ. Для виходу натисніть CTRL+C")

# Запускаємо обробку повідомлень
channel.start_consuming()
