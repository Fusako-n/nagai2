from django.urls import path
from . import views

app_name = 'translation'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('translation/', views.save_transcription, name='save_transcription'),
    #path('speech/', views.speech, name='speech'),
    #path('test/', views.save_transcription, name='save_transcription'),
]