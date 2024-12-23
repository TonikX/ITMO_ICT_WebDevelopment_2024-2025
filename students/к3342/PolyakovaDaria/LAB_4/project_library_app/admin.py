from django.contrib import admin
from .models import ReadingRoom, Book, BookCopy, Reader, BookTransaction, ReadingRoomVisit

admin.site.register(ReadingRoom)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Reader)
admin.site.register(BookTransaction)
admin.site.register(ReadingRoomVisit)
