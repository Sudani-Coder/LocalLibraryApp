from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    # path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    # path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    # path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    # path('genres/', views.GenreListView.as_view(), name='genres'),
    # path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    # path('languages/', views.LanguageListView.as_view(), name='languages'),
    # path('language/<int:pk>', views.LanguageDetailView.as_view(), name='language-detail'),
    # path('bookinstances/', views.BookInstanceListView.as_view(), name='bookinstances'),
    # path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
