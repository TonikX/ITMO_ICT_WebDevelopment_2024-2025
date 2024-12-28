## Приложение Register.
### Назначение: отвечает за логику регистрации и входа в систему.
### Модели:
```python
    class HotelBaseAccount(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(verbose_name='email_address', unique=True, max_length=200)
        firstname = models.CharField(max_length=64, null=False)
        lastname = models.CharField(max_length=64, null=False)
        date_joined = models.DateTimeField(default=timezone.now)
        birth_date = models.DateField(blank=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)
    
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['firstname', 'lastname']
    
        objects = AccountManager()
    
        @property
        def is_admin(self):
            return self.is_staff
    
        def has_perm(self, perm, obj=None):
            if perm == 'auth.can_see_residents_table':
                return self.is_staff
            return True
    
        def has_module_perms(self, app_label):
            return True
    
        def get_absolute_url(self):
            return "/account/%i/" % self.id
    
        def __str__(self):
            return f"{self.firstname} {self.lastname}. Дата рождения: {self.birth_date}. эл. почта: {self.email}"
   
```

### URLs:
```python
urlpatterns = [
    path("register/", views.CreateAccount.as_view(), name="register_account"),
    path("register/admin/", views.AdminCreateView.as_view(), name="register_admin"),
    path("login/", views.account_login, name="login"),
    path("logout/", views.account_logout, name="logout"),
]
```

### Представления:
```python
class CreateAccount(CreateView):
    model = HotelBaseAccount
    form_class = AccountCreationForm
    template_name = "register.html"
    success_url = '/'

class AdminCreateView(CreateView):
    model = HotelBaseAccount
    form_class = AdminCreationForm
    template_name = 'register.html'
    success_url = '/'

def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Invalid login form.')
        data = form.cleaned_data
        account = authenticate(email=data['email'], password=data['password'])
        if account is None or not account.is_active:
            return HttpResponse('No such account found.')
        login(request, account)
        next_url = request.session['next_url']
        del request.session['next_url']
        return redirect(next_url)
    else:
        request.session['next_url'] = get_next_url(request)
        form = LoginForm()
    return render(request, "login.html", {'form': form})


def account_logout(request):
    logout(request)
    return redirect('/')


def get_next_url(request):
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return unquote(next_url)
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=[request.get_host()]):
        return '/'
    return next_url
```