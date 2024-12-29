# Лабораторная работа 2. Реализация простого сайта на django. Вариант 5 (Список научных конференций)

---

## **1. Регистрация новых пользователей**

```python
class SignUpView(views.View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": "Регистрация",
            "form": SignUpForm(),
            "action": "Зарегистрироваться",
        }

        return render(request, "users/auth-form.html", context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Регистрация",
            "action": "Зарегистрироваться",
        }

        form = SignUpForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "users/auth-form.html", context)

        email = form.cleaned_data["email"]
        is_email_occupied = User.objects.filter(email=email).exists()
        if is_email_occupied:
            context["message"] = "Email занят другим пользователем"
            return render(request, "users/auth-form.html", context)

        User.objects.create_user(
            email=email,
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )

        return redirect(reverse("sign-in"))
```

Класс **SignUpView** наследуется от **views.View** и представляет собой представление Django для обработки регистрации пользователей. Этот класс реализует два метода: get и post, которые обрабатывают GET и POST запросы соответственно. Метод get обрабатывает GET-запросы и отображает форму регистрации. В нем создается контекст данных, который включает заголовок страницы ("Регистрация"), экземпляр формы **SignUpForm** и текст кнопки отправки формы ("Зарегистрироваться"). Затем используется функция render для отображения шаблона **users/auth-form.html** с переданным контекстом данных. Метод post обрабатывает POST-запросы, валидирует данные формы и создает нового пользователя. В нем также создается контекст данных с заголовком страницы ("Регистрация") и текстом кнопки отправки формы ("Зарегистрироваться"). Создается экземпляр формы SignUpForm с данными из запроса. Если форма не валидна, она отображается снова с ошибками. Если форма валидна, проверяется, занят ли указанный email другим пользователем. Если email занят, отображается сообщение об ошибке. Если email свободен, создается новый пользователь с указанными данными и выполняется перенаправление на страницу входа.

```html
{% extends "index.html" %} {% block title %} {{ title }} {% endblock title %} {% block content %}

<form class="auth-form" method="post">
	{% csrf_token %} {{ form.as_p }}
	<button type="submit">{{ action }}</button>
</form>

<p class="errorlist" style="text-align: center;">{{ message }}</p>

{% endblock content %}
```

Шаблон **users/auth-form.html** расширяет базовый шаблон **index.html** и используется для отображения формы аутентификации или регистрации. В шаблоне определены два блока: **title** и **content**. Блок title устанавливает заголовок страницы, используя переменную title, переданную из контекста. Блок content содержит форму с методом post, которая включает **CSRF-токен** для защиты от CSRF-атак, отображает поля формы с помощью **{{ form.as_p }}** и кнопку отправки формы с текстом, переданным в переменной action. Также в блоке **content** отображается сообщение об ошибке, если оно есть, с помощью переменной message.

## **2. Просмотр конференций и регистрацию авторов для выступлений с возможностью редактирования и удаления своих конференций.**

```python
class ConferenceListView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "conferences/conference-list.html"
    context_object_name = "conferences"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список конференций"
        return context

    def get_queryset(self):
        return Conference.objects.select_related("author").all().order_by("name")
```

Класс **ConferenceListView** наследуется от **mixins.LoginRequiredMixin** и **generic.ListView**, что позволяет использовать функциональность, требующую аутентификации пользователя, и предоставляет базовые возможности для отображения списка объектов. Атрибут template_name указывает на имя шаблона, который будет использоваться для отображения списка конференций **("conferences/conference-list.html")**. Атрибут context_object_name определяет имя переменной контекста, которая будет использоваться в шаблоне для доступа к списку конференций ("conferences"). Атрибут **paginate_by** устанавливает количество конференций, отображаемых на одной странице (1). Метод **get_context_data** переопределяет базовый метод для добавления заголовка страницы ("Список конференций") в контекст данных. Метод get_queryset возвращает отсортированный список всех конференций, используя **select_related** для оптимизации запросов к базе данных.

```python
class ConferenceDetailView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Conference
    form_class = ConferenceUpdatingForm
    template_name = "conferences/conference-detail.html"
    pk_url_kwarg = "conference_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["is_user_member"] = self.object.members.contains(self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy("conference-detail", kwargs={"conference_pk": self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(
            Conference.objects.select_related("author")
            .select_related("booking")
            .select_related("booking__room")
            .prefetch_related("members"),
            id=self.kwargs[self.pk_url_kwarg],
        )

    def form_valid(self, form):
        if self.object.author.pk != self.request.user.pk:
            raise PermissionDenied()

        return super().form_valid(form)
```

Класс **ConferenceDetailView** наследуется от **mixins.LoginRequiredMixin** и **generic.UpdateView**, что позволяет использовать функциональность, требующую аутентификации пользователя, и предоставляет базовые возможности для обновления объектов. Атрибут model указывает на модель Conference, с которой работает представление. Атрибут form_class определяет форму ConferenceUpdatingForm, которая будет использоваться для обновления конференции. Атрибут template_name указывает на имя шаблона, который будет использоваться для отображения деталей конференции **("conferences/conference-detail.html")**. Атрибут pk_url_kwarg определяет имя аргумента URL, который содержит первичный ключ конференции ("conference_pk"). Метод get_context_data переопределяет базовый метод для добавления формы обратной связи (FeedbackForm) и флага, указывающего, является ли текущий пользователь участником конференции, в контекст данных. Метод get_success_url возвращает URL для перенаправления после успешного обновления конференции, используя reverse_lazy для генерации URL на основе имени маршрута и первичного ключа конференции. Метод **get_object** переопределяет базовый метод для получения объекта конференции с использованием **get_object_or_404**, оптимизируя запросы к базе данных с помощью **select_related** и **prefetch_related**. Метод **form_valid** переопределяет базовый метод для проверки, является ли текущий пользователь автором конференции, и вызывает исключение **PermissionDenied**, если это не так. Затем вызывается родительский метод form_valid для продолжения обработки формы.

```python
class ConferenceRegistrationView(mixins.LoginRequiredMixin, views.View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {
            "form": ConferenceRegistrationForm(),
            "title": "Регистрация конференции",
            "action": "Зарегистрировать конференцию",
        }

        return render(request, "conferences/registration-form.html", context)

    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Регистрация конференции",
            "action": "Зарегистрировать конференцию",
        }

        form = ConferenceRegistrationForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "conferences/registration-form.html", context)

        booking_id = form.cleaned_data["booking"].id
        booking = Booking.objects.select_for_update(no_key=True).get(id=booking_id)
        if booking.conference is not None:
            context["message"] = "Выбранная бронь уже занята другим пользователем"
            return render(request, "conferences/registration-form.html", context)

        conference: Conference = form.save(commit=False)
        conference.author = request.user
        conference.save()

        booking.conference = conference
        booking.save()

        context["message"] = "Конференция зарегистрирована"
        context["form"] = ConferenceRegistrationForm()
        return render(request, "conferences/registration-form.html", context)
```

Класс **ConferenceRegistrationView** наследуется от **mixins.LoginRequiredMixin** и **views.View**, что позволяет использовать функциональность, требующую аутентификации пользователя, и обрабатывать GET и POST запросы. Метод get обрабатывает GET-запросы и отображает форму регистрации конференции. В нем создается контекст данных, который включает экземпляр формы **ConferenceRegistrationForm**, заголовок страницы ("Регистрация конференции") и текст кнопки отправки формы ("Зарегистрировать конференцию"). Затем используется функция render для отображения шаблона **conferences/registration-form.html** с переданным контекстом данных. Метод post обрабатывает POST-запросы, валидирует данные формы и регистрирует новую конференцию. В нем также создается контекст данных с заголовком страницы ("Регистрация конференции") и текстом кнопки отправки формы ("Зарегистрировать конференцию"). Создается экземпляр формы **ConferenceRegistrationForm** с данными из запроса. Если форма не валидна, она отображается снова с ошибками. Если форма валидна, проверяется, занята ли выбранная бронь другой конференцией. Если бронь занята, отображается сообщение об ошибке. Если бронь свободна, создается новая конференция с указанными данными и текущим пользователем в качестве автора. Затем бронь обновляется, чтобы связать ее с новой конференцией. После успешной регистрации конференции отображается сообщение об успешной регистрации и очищенная форма.

```python
class ConferenceDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Conference
    pk_url_kwarg = "conference_pk"
    success_url = reverse_lazy("conference-list")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        conference = get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])
        if conference.author.pk != request.user.pk:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
```

Класс **ConferenceDeleteView** наследуется от **mixins.LoginRequiredMixin** и **generic.DeleteView**, что позволяет использовать функциональность, требующую аутентификации пользователя, и предоставляет базовые возможности для удаления объектов. Атрибут model указывает на модель Conference, с которой работает представление. Атрибут pk_url_kwarg определяет имя аргумента URL, который содержит первичный ключ конференции ("conference_pk"). Атрибут success_url указывает URL для перенаправления после успешного удаления конференции, используя reverse_lazy для генерации URL на основе имени маршрута ("conference-list"). Метод dispatch переопределяет базовый метод для проверки, является ли текущий пользователь автором конференции, и вызывает исключение PermissionDenied, если это не так. Затем вызывается родительский метод dispatch для продолжения обработки запроса. Метод get переопределяет базовый метод для вызова метода delete, что позволяет удалять конференцию сразу при GET-запросе.

## **3. Написание отзывов к конференциям.**

```python
class FeedbackView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Feedback
    form_class = FeedbackForm

    def form_valid(self, form):
        conference = Conference.objects.filter(id=self.kwargs["conference_pk"]).first()
        if conference is None:
            raise ObjectDoesNotExist()

        is_user_member = conference.members.contains(self.request.user)
        if not is_user_member:
            raise PermissionDenied()

        if not conference.is_over():
            raise BadRequest("Конференция еще не окончена")

        feedback: Feedback = form.save(commit=False)
        feedback.author = self.request.user
        feedback.conference = conference
        feedback.save()

        redirect_url = reverse(
            "conference-detail",
            kwargs={"conference_pk": self.kwargs["conference_pk"]},
        )

        return redirect(redirect_url)
```

Класс **FeedbackView** наследуется от **mixins.LoginRequiredMixin** и **generic.CreateView**, что позволяет использовать функциональность, требующую аутентификации пользователя, и предоставляет базовые возможности для создания объектов. Атрибут model указывает на модель Feedback, с которой работает представление. Атрибут **form_class** определяет форму **FeedbackForm**, которая будет использоваться для создания отзыва. Метод form_valid переопределяет базовый метод для проверки, существует ли конференция с указанным первичным ключом, является ли текущий пользователь участником конференции и завершена ли конференция. Если конференция не существует, вызывается исключение **ObjectDoesNotExist**. Если пользователь не является участником конференции, вызывается исключение **PermissionDenied**. Если конференция еще не завершена, вызывается исключение **BadRequest** с сообщением "Конференция еще не окончена". Если все проверки пройдены, создается новый отзыв с текущим пользователем в качестве автора и указанной конференцией. Затем выполняется перенаправление на страницу деталей конференции с использованием **reverse** для генерации URL на основе имени маршрута и первичного ключа конференции.

## **4. Администратор должен иметь возможность указания результатов выступления.**

Администратор имеет статус **суперпользователя**, засчет этого ему открывается доступ к админ панеле, где он может отметить конференцию как **рекомендованную к публикации**

## **5. В клиентской части должна формироваться таблица, отображающая всех участников по конференциям.**

```html
{% extends "index.html" %} {% block title %} {{ title }} {% endblock title %} {% block content %}

<ul>
	<li>Название: {{ conference.name }}</li>
	<li>Автор: {{ conference.author }}</li>
	<li>Описание: {{ conference.description }}</li>
	<li>Условия участия: {{ conference.participation_conditions }}</li>
	<li>Начало: {{ conference.booking.start_date }}</li>
	<li>Конец: {{ conference.booking.end_date }}</li>
	<li>Конференц зал: {{ conference.booking.room }}</li>
	<li>Тематики: {{ conference.display_topics }}</li>
</ul>

<h2>Участники ({{ conference.count_members }})</h2>
<table>
	<thead>
		<tr>
			<th>Имя</th>
			<th>Фамилия</th>
			<th>Почта</th>
		</tr>
	</thead>
	<tbody>
		{% for member in conference.members.all %}
		<tr>
			<td>{{ member.first_name }}</td>
			<td>{{ member.last_name }}</td>
			<td>{{ member.email }}</td>
		</tr>
		{% endfor %}
	</tbody>
</table>

...
```

В шаблоне **conferences/conference-detail.html** отрисовывается таблица со всеми добавленными автором конференции участниками. Так как таблица конференций и участников имеет связь многие ко многим, во избежание проблемы **N + 1** в **ConferenceDetailView** был использован **prefetch_related** для предварительной подгрузки связанных записей.