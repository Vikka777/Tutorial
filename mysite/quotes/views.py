# quotes/views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Author, Quote, Tag
from .forms import RegistrationForm, LoginForm, AuthorForm, QuoteForm
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Виконайте аутентифікацію користувача тут
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

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
            quote = form.save(commit=False)  # Сохранение цитаты, но без фиксации в базе данных
            quote.user = request.user  # Привязка цитаты к текущему пользователю
            quote.save()  # Сохранение цитаты в базе данных
            return redirect('quote_list')  # Перенаправьте на страницу со списком цитат (замените 'quote_list' на имя URL-маршрута для списка цитат)
    else:
        form = QuoteForm()

    return render(request, 'add_quote.html', {'form': form})

def quotes_by_tag(request, tag):
    quotes = Quote.objects.filter(tags__name=tag)
    paginator = Paginator(quotes, 10)
    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)
    context = {'quotes': quotes, 'tag': tag}
    return render(request, 'quotes/quotes_by_tag.html', context)

def top_ten_tags(request):
    tags = Tag.objects.annotate(quote_count=Count('quote')).order_by('-quote_count')[:10]
    context = {'tags': tags}
    return render(request, 'quotes/top_ten_tags.html', context)
