import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin


def scrape_quotes(url):
    quotes_data = []
    authors_data = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.select('div.quote'):
            quote_data = {
                'quote': quote.select_one('span.text').get_text(),
                'author': quote.select_one('span small.author').get_text(),
                'tags': [tag.get_text() for tag in quote.select('div.tags a.tag')],
            }
            quotes_data.append(quote_data)

            author_data = {
                'fullname': quote_data['author'],
                'born_date': '',
                'born_location': '',
                'description': '',
            }
            authors_data.append(author_data)

        next_page = soup.select_one('li.next a')
        url = urljoin(url, next_page['href']) if next_page else None

    return quotes_data, authors_data

# Отримуємо дані
quotes, authors = scrape_quotes('http://quotes.toscrape.com/')

# Зберігаємо дані у JSON файли
with open('quotes.json', 'w') as quotes_file:
    json.dump(quotes, quotes_file, indent=2)

with open('authors.json', 'w') as authors_file:
    json.dump(authors, authors_file, indent=2)
