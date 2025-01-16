from django.db import models
import uuid

class Editor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}".strip()

class Newspaper(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название газеты")
    index = models.CharField(max_length=50, verbose_name="Индекс издания")
    price = models.FloatField(verbose_name="Цена экземпляра газеты")
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, related_name="newspapers", verbose_name="Редактор")

    def __str__(self):
        return self.name

class PrintShop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название типографии")
    address = models.TextField(verbose_name="Адрес типографии")
    is_open = models.BooleanField(default=True, verbose_name="Типография открыта")

    def __str__(self):
        return self.name

class PostOffice(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50, verbose_name="Номер почтового отделения")
    address = models.TextField(verbose_name="Адрес почтового отделения")

    def __str__(self):
        return f"Почтовое отделение №{self.number}"

class PrintRun(models.Model):
    id = models.AutoField(primary_key=True)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE, related_name="print_runs", verbose_name="Газета")
    printshop = models.ForeignKey(PrintShop, on_delete=models.CASCADE, related_name="print_runs", verbose_name="Типография")
    quantity = models.PositiveIntegerField(verbose_name="Тираж")
    date = models.DateField(verbose_name="Дата печати")

    def __str__(self):
        return f"Тираж {self.newspaper.name} - {self.date}"

class Delivery(models.Model):
    id = models.AutoField(primary_key=True)
    print_run = models.ForeignKey(PrintRun, on_delete=models.CASCADE, related_name="deliveries", verbose_name="Тираж")
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE, related_name="deliveries", verbose_name="Почтовое отделение")
    printshop = models.ForeignKey(PrintShop, on_delete=models.CASCADE, related_name="deliveries", verbose_name="Типография")
    quantity = models.PositiveIntegerField(verbose_name="Количество экземпляров")

    def __str__(self):
        return f"Доставка {self.print_run.newspaper.name} - {self.post_office.number}"