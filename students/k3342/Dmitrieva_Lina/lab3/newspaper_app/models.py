from django.db import models

# Печатная мастерская
class PrintShop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Газеты
class Newspaper(models.Model):
    name = models.CharField(max_length=255)
    index = models.CharField(max_length=20)
    editor_last_name = models.CharField(max_length=100)
    editor_first_name = models.CharField(max_length=100)
    editor_patronymic = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


# Тираж
class PrintRun(models.Model):
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    printshop = models.ForeignKey(PrintShop, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.newspaper} - {self.printshop} ({self.date})"


# Почтовое отделение
class PostOffice(models.Model):
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.number


# Доставка
class Delivery(models.Model):
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE)
    printshop = models.ForeignKey(PrintShop, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Delivery of {self.quantity} {self.newspaper} to {self.post_office}"
