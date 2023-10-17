from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

from . import models

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    # email設定→ユーザー情報を保存
    def save(self, commit=True):  # commit=FalseだとDBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user


class SearchForm(forms.Form):
    category = forms.ModelChoiceField(models.Category.objects, label='カテゴリー選択', required=False, empty_label='カテゴリー検索')
    area = forms.ModelChoiceField(models.Area.objects, label='エリア選択', required=False, empty_label='エリア選択')
    keyword = forms.CharField(label='キーワード', max_length=50, required=False)
    date = forms.DateField(label='日付', required=False)