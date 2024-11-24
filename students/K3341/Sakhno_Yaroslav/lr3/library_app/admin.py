from django.contrib import admin

from library_app.models import *

admin.site.register(BookTake)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(ReadingRoom)
admin.site.register(Reader)