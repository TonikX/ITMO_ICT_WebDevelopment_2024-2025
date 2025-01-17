from django.db import models
import uuid

class Editor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="ФИО редактора")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления редактора")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления информации")

    def __str__(self):
        return self.name

class Newspaper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название газеты")
    index = models.CharField(max_length=50, verbose_name="Индекс издания")
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, related_name="newspapers", verbose_name="Редактор")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена экземпляра газеты")
    price_updated_at = models.DateTimeField(verbose_name="Дата последнего изменения цены")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления газеты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления информации")

    def __str__(self):
        return self.name

class PrintShop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название типографии")
    address = models.TextField(verbose_name="Адрес типографии")
    is_closed = models.BooleanField(default=False, verbose_name="Статус закрытия типографии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления типографии")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления информации")

    def __str__(self):
        return self.name

class PostOffice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    office_number = models.PositiveIntegerField(verbose_name="Номер почтового отделения")
    address = models.TextField(verbose_name="Адрес почтового отделения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления почтового отделения")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления информации")

    def __str__(self):
        return f"Почтовое отделение №{self.office_number}"

class Distribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE, related_name="distributions", verbose_name="Газета")
    printshop = models.ForeignKey(PrintShop, on_delete=models.CASCADE, related_name="distributions", verbose_name="Типография")
    postoffice = models.ForeignKey(PostOffice, on_delete=models.CASCADE, related_name="distributions", verbose_name="Почтовое отделение")
    copies_printed = models.PositiveIntegerField(verbose_name="Тираж газеты в типографии")
    copies_sent = models.PositiveIntegerField(verbose_name="Количество экземпляров, отправленных в почтовое отделение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления информации")

    def __str__(self):
        return f"Распределение {self.id}"
