from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'seminar2'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', login_required(views.LoginView.as_view()), name='login'),
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
]