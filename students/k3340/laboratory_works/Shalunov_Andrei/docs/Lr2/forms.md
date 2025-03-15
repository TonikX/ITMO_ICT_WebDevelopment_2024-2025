# Формы проекта

В проекте используются различные формы для регистрации, добавления комментариев, создания профилей гонщиков и других функций. Ниже приведено описание всех форм и их полей.

---

## 1. `UserRegistrationForm`

Форма для регистрации новых пользователей. Она наследуется от стандартной модели пользователя Django и добавляет поля для ввода имени, фамилии, имени пользователя, пароля и его подтверждения.

```python
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
```
Поля:

username: имя пользователя.

first_name: имя.

last_name: фамилия.

email: электронная почта.

password: пароль.

confirm_password: подтверждение пароля.

##2. RegistrationForm
Форма для регистрации гонщика на конкретную гонку. Эта форма позволяет пользователю выбрать автомобиль, с которым он будет участвовать в гонке.

```python
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['car']
```
Поля:

car: выбор автомобиля, с которым гонщик будет участвовать в гонке.

##3. CommentForm
Форма для добавления комментариев к гонке. Включает поле для текста комментария, типа комментария и рейтинга.

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
```
Поля:

text: текст комментария.

comment_type: тип комментария (вопрос о сотрудничестве, вопрос о гонках, иное).

rating: оценка от 1 до 10.

##4. RacerProfileForm
Форма для создания профиля гонщика. Она включает такие поля, как название команды, опыт, класс гонщика, а также выбор автомобилей, которыми владеет гонщик.

```python
class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team_name', 'experience', 'racer_class']
``` 
Поля:

team_name: название команды.

experience: количество лет опыта.

racer_class: класс гонщика (например, профессионал, любитель).

##5. RacerProfileUpdateForm
Форма для редактирования профиля гонщика. Она позволяет обновлять информацию о команде, опыте и классе гонщика.

```python
class RacerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team_name', 'experience', 'racer_class']
```
Поля:

team_name: название команды.

experience: количество лет опыта.

racer_class: класс гонщика.

##6. UnregisterForm

Форма для отмены регистрации на гонку. Она не требует дополнительных полей, так как выполняет действие по аннулированию участия.

```python
class UnregisterForm(forms.Form):
    pass
```

Поля: отсутствуют, форма используется для подтверждения отмены участия.

##7. UserUpdateForm

Форма для обновления информации о пользователе. Позволяет обновлять стандартные поля модели User, такие как имя, фамилия и адрес электронной почты.

```python
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
```
Поля:

first_name: имя.

last_name: фамилия.

email: электронная почта.