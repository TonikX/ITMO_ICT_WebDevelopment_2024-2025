# Документация к формам

Этот файл описывает формы, используемые в проекте.

## 1. Форма для регистрации пользователя

```python
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'education', 'phone_number']
```

## 2. Форма для отзыва

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
```

## 3. Форма для регистрации выступления на конференции

```python
class PresentationRegistrationForm(forms.ModelForm):
    class Meta:
        model = PresentationRegistration
        fields = ['title', 'abstract']
```