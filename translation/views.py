from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
#import deepl

from .forms import TranscriptionForm, TranslationSaveForm
from .models import Translation


class TopView(TemplateView):
    template_name = 'top.html'


# def translation(request):
#     text_en = ''
#     if request.method == 'POST':
#         form = TranslationForm(request.POST)
#         if form.is_valid():
#             translator = deepl.Translator(settings.DEEPL_AUTH_KEY)
#             text_ja = form.cleaned_data['text_ja']
#             text_en = translator.translate_text(text_ja, target_lang="EN-US")
#             data = Translation(text_ja=text_ja, text_en=text_en, user=request.user)
#             if 'save' in request.POST:
#                 data.save()
#                 messages.info(request, '翻訳を保存しました')
#     else:
#         form = TranslationForm()
#     context = {'form': form, 'text_en': text_en}
#     return render(request, 'translation/translation.html', context)


from google.cloud import speech_v1p1beta1 as speech
import requests
import os


def save_transcription(request):
    if request.method == 'POST':
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']='credentials/credentials.json'
        if 'audio_file' in request.FILES:
            form = TranscriptionForm(request.POST, request.FILES)
            
            if form.is_valid():
                audio_data = form.cleaned_data['audio_file'].read()

                # Speech-to-Text APIを設定
                client = speech.SpeechClient()

                # Speech-to-Text APIに渡すRecognitionAudioを設定
                audio = speech.RecognitionAudio(content=audio_data)

                # RecognitionConfigを設定
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=44100,
                    language_code='ja-JP',
                    enable_automatic_punctuation=True,
                )

                # Speech-to-Text APIで音声をテキストに変換
                response = client.recognize(config=config, audio=audio)

                # 翻訳用にテキストを取り出す
                transcriptions = [result.alternatives[0].transcript for result in response.results]
                text_ja = ' '.join(transcriptions)

                # DeepL APIでテキストを翻訳
                deepl_api_key = settings.DEEPL_AUTH_KEY
                deepl_api_url = 'https://api-free.deepl.com/v2/translate'
                params = {
                    'auth_key': deepl_api_key,
                    'text': text_ja,
                    'source_lang': 'ja',
                    'target_lang': 'en',
                }
                translation_response = requests.post(deepl_api_url, data=params)
                text_en = translation_response.json()['translations'][0]['text']
                
                context = {
                    'text_ja': text_ja,
                    'text_en': text_en,
                    'translation_form': TranslationSaveForm()}
                
                return render(request, 'translation/translation.html', context)
            
        elif 'text_ja' in request.POST and 'text_en' in request.POST:
            translation_form = TranslationSaveForm(request.POST)
            if translation_form.is_valid():
                text_ja = request.POST['text_ja']
                text_en = request.POST['text_en']
                data = Translation(text_ja=text_ja, text_en=text_en, user=request.user)
                data.save()
                messages.info(request, '翻訳を保存しました')

                return render(request, 'translation/translation.html', {
                    'form': TranscriptionForm(),
                    'translation_form': TranslationSaveForm()})

    else:
        form = TranscriptionForm()
        return render(request, 'translation/translation.html', {'form': form})