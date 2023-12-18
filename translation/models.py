from django.db import models
from django.contrib.auth import get_user_model


class Translation(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='ユーザー', on_delete=models.CASCADE)
    text_ja = models.TextField(verbose_name='テキスト日本語')
    text_en = models.TextField(verbose_name='テキスト英語')
    audio_file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text_ja[:20]