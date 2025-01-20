#Используемые модели:

## Клиент
```python
class Client(models.Model):
    """
    Описание модели физического лица/сотрудника фирмы
    """
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    risk_category = models.CharField(max_length=10,
                                     choices=RISK_CATEGORY_CHOICES)

    def __str__(self):
        return self.name
```

## Специализации
```python
class Specialization(models.Model):
    """
    Специализация компаний
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
```

## Компании
```python
class Enterprise(models.Model):
    """
    Описание компании
    """
    code = models.IntegerField()
    full_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=150, null=True)
    bank_details = models.IntegerField()
    specialization = models.ManyToManyField("Specialization")

    def __str__(self):
        return self.short_name
```

## Трудовые договоры
```python
class EmploymentContract(models.Model):
    """
    Трудовой договор с агентом
    """
    start_date = models.DateField()
    end_date = models.DateField(null=True)
```

## Страховые агенты
```python
class Agent(AbstractUser):
    """
    Страховой агент
    """
    passport_number = models.IntegerField()
    phone_number = models.IntegerField()
    contract = models.ForeignKey("EmploymentContract",
                                 on_delete=models.CASCADE, null=True)

    groups = models.ManyToManyField('auth.Group',
                                    related_name='insurance_agents',
                                    blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',
                                              related_name='insurance_agents',
                                              blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'contract',
                       'passport_number']
```

## Возможные выплаты
```python
class Payout(models.Model):
    """
    Возможные выплаты с суммами
    """

    EVENT_CATEGORY_CHOICES = [
        ('light', 'Легкое происшествие'),
        ('middle', 'Происшествие средней тяжести'),
        ('highest', 'Происшествие высокой степени тяжести'),
    ]

    risk_category = models.CharField(max_length=10,
                                     choices=RISK_CATEGORY_CHOICES)
    sum = models.IntegerField()
    insured_event = models.CharField(max_length=10,
                                     choices=EVENT_CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.risk_category}, sum - {self.sum}"
```

## Страховые договоры
```python
class InsuranceContract(models.Model):
    """
    Страховой договор
    """
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    signing_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()

    TYPE_CHOICES = [
        ("ind", "Индивидуальный"),
        ("col", "Коллективный")
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    available_payouts = models.ManyToManyField("Payout")
    enterprise = models.ForeignKey("Enterprise", on_delete=models.CASCADE,
                                   null=True)
    participating_persons = models.ManyToManyField("Client")
```

## Выплаты по страховым случаям
```python
class InsuranceClaim(models.Model):
    insurance_contract = models.ForeignKey("InsuranceContract", on_delete=models.CASCADE)
    date_occured = models.DateField()
    reason = models.CharField(max_length=200)
    decision = models.BooleanField()
    payout_amount = models.IntegerField(null=True)
```