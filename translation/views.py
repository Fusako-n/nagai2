from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
import deepl

from .forms import TranscriptionForm
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
            text_to_translate = ' '.join(transcriptions)

            # DeepL APIでテキストを翻訳
            deepl_api_key = settings.DEEPL_AUTH_KEY
            deepl_api_url = 'https://api-free.deepl.com/v2/translate'
            params = {
                'auth_key': deepl_api_key,
                'text': text_to_translate,
                'source_lang': 'ja',
                'target_lang': 'en',
            }
            translation_response = requests.post(deepl_api_url, data=params)
            translated_text = translation_response.json()['translations'][0]['text']
            
            data = Translation(text_ja=text_to_translate, text_en=translated_text, user=request.user)
            if 'save' in request.POST:
                data.save()
                messages.info(request, '翻訳を保存しました')

            context = {
                'text_ja': text_to_translate,
                'text_en': translated_text,
            }

            return render(request, 'translation/translation.html', context)

    else:
        form = TranscriptionForm()
    return render(request, 'translation/translation.html', {'form': form})