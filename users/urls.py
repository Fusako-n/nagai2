from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('mypage/<int:pk>/', views.MypageView.as_view(), name='mypage'),
    path('mypage_edit/<int:pk>/', views.MypageEditView.as_view(), name='mypage_edit'),
]