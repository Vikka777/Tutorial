from mongoengine import Document, connect, StringField, ListField, ReferenceField, DateTimeField
import json

# Подключение к базе данных
connect('cluster0', host='mongodb+srv://vikkimrrr7:VikaVika78@cluster0.kvolsxm.mongodb.net/')

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

def insert_data(collection_name, data):
    for item in data:
        collection_name(**item).save()

# Загрузка данных из authors.json
with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)
    insert_data(Author, authors_data)

# Загрузка данных из quotes.json
with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)
    insert_data(Quote, quotes_data)

# Создание скрипта для поиска цитат
def search_quotes():
    while True:
        command = input("Введите команду: ").strip().lower()
        if command == "exit":
            print("Скрипт завершен.")
            break
        elif command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            author = Author.objects(name=author_name).first() # type: ignore
            if author is not None:
                quotes = Quote.objects(author=author) # type: ignore
                for quote in quotes:
                    print(quote.text)
            else:
                print("Автор не найден")
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = Quote.objects(tags__in=[tag]) # type: ignore
            for quote in quotes:
                print(quote.text)
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(',')
            quotes = Quote.objects(tags__in=tags) # type: ignore
            for quote in quotes:
                print(quote.text)
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    search_quotes()

