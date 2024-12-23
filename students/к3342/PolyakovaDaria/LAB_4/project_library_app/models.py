from django.db import models


class ReadingRoom(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (#{self.number})"


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    section = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    is_discarded = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    room = models.ForeignKey(ReadingRoom, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.book.title} in {self.room.name}"


class Reader(models.Model):
    ticket_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    education_level = models.CharField(max_length=50)
    has_academic_degree = models.BooleanField(default=False)
    assigned_room = models.ForeignKey(ReadingRoom, on_delete=models.SET_NULL, null=True)
    registration_date = models.DateField()
    re_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class BookTransaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=20)
    due_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_type} of {self.book.title} by {self.reader.full_name}"


class ReadingRoomVisit(models.Model):
    room = models.ForeignKey(ReadingRoom, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    duration_min = models.IntegerField()

    def __str__(self):
        return f"Visit by {self.reader.full_name} to {self.room.name} on {self.visit_date}"
