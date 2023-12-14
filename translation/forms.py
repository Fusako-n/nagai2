from django import forms

from .models import Upload


class TranslationForm(forms.Form):
    text_ja = forms.CharField(label='文章を入力（日本語）', required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text_ja'].widget = forms.Textarea(attrs={'class': 'form-control', 'id': 'Textarea1'})


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['text']