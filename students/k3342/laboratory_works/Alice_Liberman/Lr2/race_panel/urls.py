from django.contrib import admin
from django.urls import path

from .views.account import (LoginRacerView,
                            RacerAccountView,
                            RegisterRacerView,
                            LogoutRacerView)
from .views.cars import RacerCarView, CarUpdateView, CarDeleteView, CarCreateView
from .views.navigation import (RootView,
                               AboutView)
from .views.race import RaceListView, RaceDetailView, RegistrationCreateView, RegistrationDeleteView, YourRaceListView, \
    HistoryRaceListView, CommentCreate

urlpatterns = [
    # base pages
    path("", RootView.as_view(), name="root"),
    path('about/', AboutView.as_view(), name="about"),

    # account management
    path('account/', RacerAccountView.as_view(), name="account"),
    path('account/login/', LoginRacerView.as_view(), name="login"),
    path('account/register/', RegisterRacerView.as_view(), name="register"),
    path('account/logout/', LogoutRacerView.as_view(), name="register"),

    # car management
    path('cars/', RacerCarView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarUpdateView.as_view(), name="edit_car"),
    path('cars/delete/<int:pk>/', CarDeleteView.as_view(), name="delete_car"),
    path('cars/register/', CarCreateView.as_view(), name="create_car"),

    # race management
    path('race/', RaceListView.as_view(), name="race"),  # add comments and social stuff
    path('race/<int:pk>/', RaceDetailView.as_view(), name="race_info"),
    path('race/<int:pk>/register/', RegistrationCreateView.as_view(), name="register_race"),
    path('race/<int:pk>/delete/', RegistrationDeleteView.as_view(), name="delete_registration"),
    path('race/<int:pk>/comment/', CommentCreate.as_view(), name="create_comment"),

    path('race/yours/', YourRaceListView.as_view(), name="yours"),
    path('race/history/', HistoryRaceListView.as_view(), name="history"),

    # social

    # admin panel
    path("admin/", admin.site.urls),

]
