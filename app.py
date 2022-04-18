import os
from xml.etree.ElementTree import Comment
from click import command
from google.cloud import texttospeech
import io
import streamlit as st
from sympy import content
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/salib/udemy/text_speech/future-linker-344511-3be9cc6bff4a.json'

def synthesize_speech(text, lang='日本語', gender='defalut'):
    gender_type = {
        'defalut': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }

    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

st.title('音声出力アプリ')
st.markdown('### データ準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力','テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力して下さい。', 'こちらは、サンプル文になります。', height=250)
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードして下さい。', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')
    
    lang = st.selectbox(
        '言語を選択して下さい',
        ('日本語', '英語')
    )
    gender = st.selectbox(
        '話者の性別選択を選択して下さい',
        ( 'defalut', 'male', 'female', 'neutral')
    )
    st.markdown('### 音声合成')
    st.write('合成を開始しますか？')
    if st.button('開始'):
        Comment = st.empty()
        Comment.write ('音声出力を開始します')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        Comment.write('完了しました')
        
    