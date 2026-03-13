from django.contrib import admin
from .models import ReadingRoom, Reader, Book, Borrowing

admin.site.register(ReadingRoom)
admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Borrowing)