from django.contrib import admin
from django.urls import path, include
from hotel import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hotels/", include("hotel.urls")),
    path("", urls.views.home_view),
    path("register/", urls.views.register, name="register"),
    path("login/", urls.views.login_view, name="login"),
    path("logout/", urls.views.logout_view, name="logout"),
]
