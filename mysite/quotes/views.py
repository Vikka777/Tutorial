from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Author, Quote, Tag
from .forms import RegistrationForm, LoginForm, AuthorForm, QuoteForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

def scrape_quotes(request):
    # Ваш код для витягування цитат з сайту
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("span", class_="small")
        tags = soup.find_all("a", class_="tag")

        for quote, author, tag in zip(quotes, authors, tags):
            quote_text = quote.get_text()
            author_name = author.get_text()
            tag_name = tag.get_text()

            # Збереження автора, цитати і тега в базу даних
            author, created = Author.objects.get_or_create(name=author_name)
            quote = Quote.objects.create(text=quote_text, author=author)
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

    return redirect('quote_list')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('quote_list')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})

# Додамо функцію для відображення цитат з пагінацією
def quote_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # 10 цитат на сторінку
    page = request.GET.get('page')

    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'quotes/quote_list.html', {'quotes': quotes})

# Додамо функцію для відображення списку тегів з пагінацією
def top_ten_tags(request):
    tags = Tag.objects.annotate(quote_count=Count('quote')).order_by('-quote_count')
    paginator = Paginator(tags, 10)  # 10 тегів на сторінку
    page = request.GET.get('page')

    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        tags = paginator.page(paginator.num_pages)

    return render(request, 'quotes/top_ten_tags.html', {'tags': tags})
