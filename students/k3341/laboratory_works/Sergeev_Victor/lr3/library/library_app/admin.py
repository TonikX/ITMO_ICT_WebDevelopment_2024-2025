from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookGenre)
admin.site.register(BookAuthor)
admin.site.register(BookCopy)
admin.site.register(ReadingRoom)
admin.site.register(Reader)
admin.site.register(BookTake)

# Register your models here.
