from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import Login, Logout

app_name = 'accounts'

urlpatterns = [
    
    path('login/', Login.as_view(), name='login'),
    path ('logout/', Logout.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
