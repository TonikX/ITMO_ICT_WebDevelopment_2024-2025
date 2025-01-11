from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from racestable.forms import LoginForm, RegistrationForm, RacerForm, UserUpdateForm, CommentForm, RaceConnectionForm

# Create your views here.
from racestable.models import Race, Comment, RaceConnection


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
