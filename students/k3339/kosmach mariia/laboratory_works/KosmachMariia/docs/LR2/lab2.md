# Лабораторная работа №2

Табло должно отображать информацию об участниках автогонок: ФИО участника,
название команды, описание автомобиля, описание участника, опыт и класс участника.
Необходимо реализовать следующий функционал:
- Регистрация новых пользователей.
- Просмотр автогонок и регистрацию гонщиков. Пользователь должен иметь
возможность редактирования и удаления своих регистраций.
- Написание отзывов и комментариев к автогонкам. Предварительно
комментатор должен зарегистрироваться. При добавлении комментариев
должны сохраняться даты заезда, текст комментария, тип комментария
(вопрос о сотрудничестве, вопрос о гонках, иное), рейтинг (1-10),
информация о комментаторе.
- Администратор должен иметь возможность указания времени заезда и
результата средствами Django-admin.
- В клиентской части должна формироваться таблица всех заездов и
результатов конкретной гонки.

## Ход выполнения работы

### models.py:

    class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    has_racer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    class Racer(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        team = models.CharField(max_length=100)
        car = models.CharField(max_length=100)
        description = models.TextField()
        experience = models.IntegerField()
        type = models.CharField(max_length=100)


    class Race(models.Model):
        name = models.CharField(max_length=100)
        date = models.DateTimeField()
        winner = models.ForeignKey(Racer, on_delete=models.SET_NULL, blank=True, null=True)
    
        def __str__(self):
            return f"{self.name}"


    class RaceConnection(models.Model):
        racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
        race = models.ForeignKey(Race, on_delete=models.CASCADE)
    
        class Meta:
            unique_together = ('racer', 'race')
    
    
    class Comment(models.Model):
        COMMENT_TYPES = (
            ("cooperation", "Сотрудничество"),
            ("race", "Гонка"),
            ("other", "Другое")
        )
        race = models.ForeignKey(Race, on_delete=models.CASCADE)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        text = models.TextField()
        comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES)
        rating = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(10)]
        )
        created_at = models.DateTimeField(auto_now_add=True)

### views.py:

    def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


    def user_login(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('profile')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login or password')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    
    def registration(request):
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                return redirect("login")
        else:
            form = RegistrationForm()
    
        return render(request, "registration.html", {"user_form": form})
    
    
    def index(request):
        return render(request, "index.html")
    
    
    @login_required
    def profile(request):
        return render(request, 'profile.html', {'section': 'profile', 'has_racer': hasattr(request.user, 'racer')})
    
    
    @login_required
    def racer_registration(request):
        user = request.user
        print(user.has_racer)
        if hasattr(request.user, "racer"):
            return HttpResponse("You have already got a racer")
        else:
            if request.method == "POST":
    
                racer_form = RacerForm(request.POST)
                if racer_form.is_valid():
                    print(user)
                    racer = racer_form.save(commit=False)
                    racer.user = user
                    racer.save()
                    user.has_racer = True
                    user.save()
                    return redirect("profile")
            else:
                racer_form = RacerForm()
    
        return render(request, "racer_registration.html", {"racer_form": racer_form})
    
    
    @login_required
    def edit_user(request):
        if request.method == "POST":
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        else:
            user_form = UserUpdateForm(instance=request.user)
        return render(request, "edit_user.html", {"user_form": user_form}, )
    
    
    @login_required
    def change_password(request):
        if request.method == "POST":
            password_form = PasswordChangeForm(request.user, request.POST)
    
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect("profile")
        else:
            password_form = PasswordChangeForm(request.user)
        return render(request, "change_password.html", {"password_form": password_form, })
    
    
    @login_required()
    def edit_racer(request):
        if request.method == "POST":
            racer_form = RacerForm(request.POST, instance=request.user.racer)
            if racer_form.is_valid():
                racer_form.save()
                return redirect("profile")
        else:
            if hasattr(request.user, "racer"):
                racer_form = RacerForm(instance=getattr(request.user, "racer", None))
            else:
                racer_form = None
        return render(request, "edit_racer.html", {"racer_form": racer_form, })
    
    
    @login_required
    def race_comments(request, race_id):
        race = get_object_or_404(Race, id=race_id)
        comments = Comment.objects.filter(race=race)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.race = race
                comment.author = request.user
                comment.save()
        else:
            form = CommentForm()
        return render(request, "race_comments.html", {"race": race, "comments": comments, "form": form})
    
    
    @login_required
    def races_list(request):
        races = Race.objects.all()
        race_connections = RaceConnection.objects.filter(racer=request.user.racer).values("race")
        # print(race_connections)
        racer_races = []
        for race_connection in race_connections:
            racer_races.append(race_connection['race'])
        # print(racer_races)
        return render(request, "races_list.html", {"races": races, "race_connections": racer_races})
    
    
    @login_required
    def delete_account(request):
        if request.method == "POST":
            request.user.delete()
            return redirect("index")
        return render(request, "delete_account.html")
    
    
    @login_required
    def create_race_connection(request, race_id):
        user = request.user
        if not (hasattr(user, "racer")):
            return HttpResponse("You have not got a racer")
        else:
            try:
                race_connection = RaceConnection()
                race = Race.objects.get(pk=race_id)
                race_connection.race = race
                race_connection.racer = user.racer
                race_connection.save()
            except Exception as ex:
                print(ex)
                return HttpResponse('You have already registrated')
            return redirect("races_list")
        return redirect("races_list")
    
    
    def delete_race_connection(request, race_id):
        racer = request.user.racer
        race = Race.objects.get(pk=race_id)
        RaceConnection.objects.filter(racer=racer, race=race).delete()
        return redirect("races_list")

### forms.py:
    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)
    
    
    class RegistrationForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ["username", "password", "first_name", "last_name"]
    
    
    class RacerForm(forms.ModelForm):
        class Meta:
            model = Racer
            fields = ["team", "car", "description", "experience", "type"]
    
    
    class UserUpdateForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ["first_name", "last_name"]
    
    
    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ["comment_type", "rating", "text"]
    
    
    class RaceConnectionForm(forms.ModelForm):
        class Meta:
            model = RaceConnection
            fields = ["race"]

### urls.py:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("", views.index, name="index"),
        path('login/', views.user_login, name='login'),
        path('logout/', views.user_logout, name='logout'),
        path('profile/', views.profile, name='profile'),
        path("registration/", views.registration, name="registration"),
        path("racer_registration/", views.racer_registration, name="racer_registration"),
        path("edit_user/", views.edit_user, name="edit_user"),
        path("change_password/", views.change_password, name="change_password"),
        path("edit_racer/", views.edit_racer, name="edit_racer"),
        path("races/comments/<int:race_id>/", views.race_comments, name="race_comments"),
        path("races/", views.races_list, name="races_list"),
        path("profile/delete/", views.delete_account, name="delete_account"),
        path("create_race_connection/<int:race_id>/", views.create_race_connection, name="create_race_connection"),
        path("delete_race_connection/<int:race_id>", views.delete_race_connection, name="delete_race_connection")
    ]

## Результат

### Главная страница:

![Результат](images/1.png)

### Страница регистрации:

![Результат](images/2.png)

### Страница авторизации:

![Результат](images/3.png)

### Профиль:

![Результат](images/4.png)

### Редактирование пользователя:

![Результат](images/5.png)

### Смена пароля:

![Результат](images/6.png)

### Регистрация гонщика:

![Результат](images/7.png)

### Редактирование гонщика:

![Результат](images/8.png)

### Создание гонки:

![Результат](images/9.png)

### Список гонок:

![Результат](images/10.png)

### Регистрация на гонку:

![Результат](images/11.png)

### Отмена регистрации на гонку:

![Результат](images/12.png)

### Добавление комментария к гонке:

![Результат](images/13.png)

### Просмотр комментариев к гонке:

![Результат](images/14.png)

### Выбор победителя гонки:

![Результат](images/15.png)

### Просмотр победителя гонки:

![Результат](images/16.png)

### Выход из профиля:

![Результат](images/17.png)

### Удаление аккаунта:

![Результат](images/18.png)