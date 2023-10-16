# quotes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('top_ten_tags/', views.top_ten_tags, name='top_ten_tags'),
    path('quotes_by_tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),

]
