from django.urls import path
from . import views

app_name = 'translation'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('translation/', views.translation, name='translation'),
    path('speech/', views.speech, name='speech'),
]