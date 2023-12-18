from django import forms


class TranslationSaveForm(forms.Form):
    pass


class TranscriptionForm(forms.Form):
    audio_file = forms.FileField(label='音声データをアップロード')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs['class'] = 'form-control'
