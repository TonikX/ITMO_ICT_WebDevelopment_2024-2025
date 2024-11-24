### 1. Выведете все машины марки “Toyota”
**Листинг**
```python
Car.objects.filter(brand='Toyota')
```

**Результат**
<br>
![img_1.png](img/img_1.png)

### 2. Найти всех водителей с именем “Олег”
**Листинг**
```python
Owner.objects.filter(first_name='Олег')
```

**Результат**
<br>
![img_2.png](img/img_2.png)

### 3. Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели
**Листинг**
```python
random_driver = (Owner.objects.order_by('?').first())
DriverLicense.objects.get(owner_id=random_driver)
```

**Результат**
<br>
![img_3.png](img/img_3.png)

### 4. Вывести всех владельцев красных машин
**Листинг**
```python
Owner.objects.filter(cars__color='Red').distinct()
```

**Результат**
<br>
![img_4.png](img/img_4.png)

### 5. Найти всех владельцев, чей год владения машиной начинается с 2010
**Листинг**
```python
Owner.objects.filter(ownership__start_date__year=2010).distinct()
```

**Результат**
<br>
![img_5.png](img/img_5.png)