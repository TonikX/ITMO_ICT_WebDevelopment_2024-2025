from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_staff']


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'surname', 'name', 'patronymic']


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'publisher', 'cipher']


class LibraryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']


class HallAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'capacity', 'library']


class ReaderAdmin(admin.ModelAdmin):
    list_display = ['id', 'surname', 'name', 'patronymic', 'ticket', 'passport', 'birth_date', 'address', 'phone', 'education', 'is_academic', 'hall']


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'author']


class BookReaderAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'reader', 'start_date', 'end_date']


class BookHallAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'hall', 'count']


admin.site.register(User, UserAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReader, BookReaderAdmin)
admin.site.register(BookHall, BookHallAdmin)
