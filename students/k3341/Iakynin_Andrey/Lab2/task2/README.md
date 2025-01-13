# Задание 1: Авто.ру

## Краткое описание задания

Сдлелай пункты 2.1,  2.2 , 2.3

## Models

```python
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class OwnerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Owner(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=30, null=False, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=True)
    birth_date = models.DateField(null=False)
    passport_number = models.CharField(max_length=20, null=False, blank=False, unique=True)
    home_address = models.CharField(max_length=20, null=False, blank=False)
    nationality = models.CharField(max_length=20, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'birth_date', 'passport_number', 'home_address', 'nationality']

    objects = OwnerManager()

    def __str__(self):
        return self.email


class Car(models.Model):
    state_num = models.CharField(max_length=15, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=30, null=False, blank=False)
    owners = models.ManyToManyField(
        Owner,
        through="Ownership",
        related_name="cars",
    )

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_id = models.CharField(max_length=10, null=False, blank=False, unique=True)
    type = models.CharField(max_length=10, null=False, blank=False)
    license_date = models.DateField(null=True, blank=True)
```

1) Owner: Пользовательская модель владельца, расширяющая AbstractUser. Она использует email вместо имени пользователя (с полем USERNAME_FIELD). Включает дополнительные поля, такие как фамилия, имя, дата рождения, номер паспорта, адрес и гражданство. Также определены методы для создания пользователя и суперпользователя через OwnerManager.

2) Car: Модель для автомобилей, включает поля для регистрационного номера, марки, модели и цвета. Связана с моделью владельцев через промежуточную модель Ownership.

3) Ownership: Промежуточная модель, которая связывает владельцев с их автомобилями и хранит информацию о периоде владения автомобилем (дата начала и окончания).

4) DriverLicense: Модель для водительских прав владельца с уникальным номером лицензии, типом и датой получения.

## Views
```view
class CarCreateView(CreateView):
    model = Car
    fields = [
        'state_num',
        'brand',
        'model',
        'color'
    ]
    template_name = 'add_car.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
    model = Car
    success_url = reverse_lazy('car_list')
    template_name = 'delete_car.html'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['state_num', 'brand', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

    def get_object(self, queryset=None):
        car_id = self.kwargs.get('pk')
        car = Car.objects.filter(pk=car_id).first()
        if not car:
            raise Http404(f"Car with id {car_id} does not exist")
        return car
```

Эти представления обрабатывают создание, удаление и редактирование записей автомобилей в базе данных:

- CarCreateView: Обеспечивает создание нового автомобиля. Использует форму с полями для регистрационного номера, марки, модели и цвета, а после успешного создания перенаправляет на список автомобилей (car_list).

- CarDeleteView: Позволяет удалять автомобиль и после удаления перенаправляет на список автомобилей. Использует шаблон delete_car.html.

- CarUpdateView: Обеспечивает редактирование данных автомобиля. Если автомобиль с указанным pk не найден, вызывает ошибку Http404.






# Задание 2: Список отелей

## Краткое описание задания

  Необходимо реализовать следующий функционал:
1) Регистрация новых пользователей.
2) Просмотр и резервирование номеров. Пользователь должен иметь возможность редактирования и удаления своих резервирований.
4) Написание отзывов к номерам. При добавлении комментариев, должны
сохраняться период проживания, текст комментария, рейтинг (1-10),
информация о комментаторе.
5) Администратор должен иметь возможность заселить пользователя в отель и
выселить из отеля средствами Django-admin.
6) В клиентской части должна формироваться таблица, отображающая
постояльцев отеля за последний месяц.

## Стек реализации

- Язык: Python
- Программное обеспечение: Python 3.6+, Django 3

## Models

```python
class Hotel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_hotels")
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    favorites = models.ManyToManyField(User, related_name="favorite_hotels", blank=True)


class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    SUITE = 'Suite'
    FAMILY = 'Family'

    ROOM_TYPE_CHOICES = [
        (SINGLE, 'Одноместный'),
        (DOUBLE, 'Двухместный'),
        (SUITE, 'Люкс'),
        (FAMILY, 'Семейный'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_hotels')
    type = models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES, default=SINGLE)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_owner = models.BooleanField(default=False)
```
- Hotel: Модель отеля с полями для названия, владельца, адреса, описания и списка избранных пользователей.
- oom: Модель комнаты, связанная с отелем, с типом (одноместный, двухместный, люкс, семейный) и ценой.
- Booking: Модель бронирования, которая включает пользователя, комнату, дату заезда и выезда.
- Review: Модель отзыва пользователя о комнате с текстом и оценкой.
- Profile: Модель профиля пользователя, содержащая информацию о том, является ли он владельцем отеля.

Этот код реализует две функции для авторизации и регистрации пользователей:


## Views
```view
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration_form.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('hotel_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form = UserLoginForm()
        return render(request, 'account/login.html', {'form': form})
```


1) register: Обрабатывает регистрацию нового пользователя. Если форма с данными пользователя корректна, создается новый пользователь, пароль шифруется, и пользователь сохраняется в базе данных. После этого происходит редирект на страницу логина.


2) user_login: Обрабатывает вход пользователя. При успешной проверке данных (пользователь существует и пароль правильный) происходит вход в систему, и пользователя перенаправляют на страницу списка отелей. В случае неуспешного входа выводится сообщение об ошибке.

