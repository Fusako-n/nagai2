from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
import deepl

from .forms import TranslationForm, UploadForm
from .models import Translation, Upload


class TopView(TemplateView):
    template_name = 'top.html'


def translation(request):
    text_en = ''
    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            translator = deepl.Translator(settings.DEEPL_AUTH_KEY)
            text_ja = form.cleaned_data['text_ja']
            text_en = translator.translate_text(text_ja, target_lang="EN-US")
            data = Translation(text_ja=text_ja, text_en=text_en, user=request.user)
            if 'save' in request.POST:
                data.save()
                messages.info(request, '翻訳を保存しました')
    else:
        form = TranslationForm()
    context = {'form': form, 'text_en': text_en}
    return render(request, 'translation/translation.html', context)


def speech(request):
    import os
    import subprocess
    
    #保存PATH
    source = 'media'  # ファイルがアップロードされるpath

    #GCS_URL
    GCS_BASE = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'   

    #結果保存
    speech_result = ''

    if request.method == 'POST':
        #GoogleStorageの環境準備
        from google.cloud import storage
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='jsonのPATH'
        client = storage.Client()
        bucket = client.get_bucket('GoogleStorageのバケット名')

        #アップロードファイルの保存
        form = UploadForm(request.POST,request.FILES)
        form.save()

        #アップロードしたファイル名を取得
        #ファイル名と拡張子を分割(ext->拡張子(.py))
        transcribe_file = request.FILES['document'].name
        name, ext = os.path.splitext(transcribe_file)

        if ext==".wav": 
            #GoogleStorageへアップロード
            blob = bucket.blob( transcribe_file )
            blob.upload_from_filename(filename= source + transcribe_file )

            #再生時間を取得
            from pydub import AudioSegment
            sound = AudioSegment.from_file( source + transcribe_file )
            length = sound.duration_seconds
            length += 1


            #作業用ファイルの削除
            cmd = 'rm -f ' + source + transcribe_file     
            subprocess.call(cmd, shell=True)

            #文字起こし
            from google.cloud import speech

            client = speech.SpeechClient()
            gcs_uri = GCS_BASE + transcribe_file
            audio = speech.RecognitionAudio(uri=gcs_uri)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                #sample_rate_hertz=16000,
                language_code='ja_JP',
                enable_automatic_punctuation=True,
            )

            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=round(length))

            for result in response.results:
                speech_result += result.alternatives[0].transcript

            #GoogleStorageのファイル削除
            blob.delete()

        else:
            #ファイルの変換処理
            f_input = source + transcribe_file
            f_output = source + name + '.wav'
            upload_file_name = name + '.wav'
            cmd = 'ffmpeg -i ' + f_input + ' -ar 16000 -ac 1 ' + f_output
            subprocess.call(cmd, shell=True)

            #GoogleStorageへアップロード
            blob = bucket.blob( upload_file_name )
            blob.upload_from_filename(filename= f_output )

            #再生時間を取得
            from pydub import AudioSegment
            sound = AudioSegment.from_file( source + transcribe_file )
            length = sound.duration_seconds
            length += 1

            #作業用ファイルの削除
            cmd = 'rm -f ' + f_input + ' ' + f_output     
            subprocess.call(cmd, shell=True)

            #文字起こし
            from google.cloud import speech

            client = speech.SpeechClient()
            gcs_uri = GCS_BASE + upload_file_name
            audio = speech.RecognitionAudio(uri=gcs_uri)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                #sample_rate_hertz=16000,
                language_code='ja_JP',
            )

            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=round(length))

            for result in response.results:
                speech_result += result.alternatives[0].transcript

            #GoogleStorageのファイル削除
            blob.delete()
    else:
        form = UploadForm()
    return render(request, 'translation/speech.html', {
        'form': form,
        'transcribe_result':speech_result
    })