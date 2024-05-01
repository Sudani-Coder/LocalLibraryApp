from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration object for Author models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('author', 'genre', 'language')
    # inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

admin.site.register(Genre)
admin.site.register(Language)

"""Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)
"""
