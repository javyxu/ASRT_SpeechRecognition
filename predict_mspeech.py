# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2020-02-15 19:17:05
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: predict_mspeech.py
'''

import os
import wave
from datetime import datetime
from pyaudio import PyAudio, paInt16

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=10

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    with wave.open(filename,'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(b"".join(data))

def my_record(vedio_file):
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count < TIME * 3:   # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file(vedio_file, my_buf)
    stream.close()


chunk=2014
def play(vedio_file):
    wf=wave.open(vedio_file,'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":
            break
        stream.write(data)
    stream.close()
    p.terminate()


def predict(video_file):
    from SpeechModel251 import ModelSpeech
    from LanguageModel2 import ModelLanguage
    from keras import backend as K

    datapath = 'dataset'
    modelpath = 'model_speech'

    ms = ModelSpeech(datapath)
    ms.LoadModel(modelpath + '/m251/speech_model251_e_0_step_60500.model')

    pinyin = ms.RecognizeSpeech_FromFile(video_file)
    K.clear_session()

    ml = ModelLanguage('model_language')
    ml.LoadModel()

    str_pinyin = pinyin
    text = ml.SpeechToText(str_pinyin)
    return pinyin, text

def text2sppech(text):
    import pyttsx3
    engine = pyttsx3.init()
    # voices = engine.getProperty("voices")
    # for item in voices:
    #     print(item.id,item.languages)
    # macos
    # com.apple.speech.synthesis.voice.ting-ting
    # windows
    # "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
    voices = ['com.apple.speech.synthesis.voice.ting-ting', 
              'com.apple.speech.synthesis.voice.mei-jia',
              'com.apple.speech.synthesis.voice.sin-ji']
    engine.setProperty('voice', voices[0])
    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == '__main__':
    vedio_file = str(datetime.now().timestamp()) + ".wav"
    my_record(vedio_file)
    print("录音结束")
    # print("开始播放录音")
    # play(vedio_file)
    # print("播放录音结束")
    pinyin, text = predict(vedio_file)
    print('语音转文字结果：\n', text)
    os.remove(vedio_file)
    text2sppech(text)