from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', RedirectView.as_view(url='/homework/', permanent=False), name='home'),
    
    path('accounts/', include('accounts.urls')),
    path('homework/', include('homework.urls')),
]