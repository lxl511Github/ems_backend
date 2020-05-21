from django.conf.urls import url
import Books.views as views

urlpatterns = [
    url(r'add_book', views.add_book),
    url(r'show_books', views.show_books),
]
