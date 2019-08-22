import boto3
from pygame import mixer
import time
import speech_recognition as sr

lex = boto3.client('lex-runtime', region_name='us-west-2')
polly = boto3.client('polly', region_name='us-west-2')
mixer.init()
rec = sr.Recognizer()
output = 1


def listen():
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source)
        print('say now')
        audio = rec.listen(source, phrase_time_limit=2)
        print('response')
        speech = rec.recognize_google(audio, language='en', show_all=True)
        print(speech)
        if 'alternative' in speech and speech['alternative'][0] and 'transcript' in speech['alternative'][0]:
            ask_lex(speech['alternative'][0]['transcript'])
        print('thanks done')
        listen()


def ask_lex(text):
    global output
    lex_response = lex.post_text(
        botName='BotVoiceControl',
        botAlias='BulldogBotVoiceControl',
        userId='bot01',
        sessionAttributes={},
        requestAttributes={},
        inputText=text
    )
    if 'slots' in lex_response and 'Direction' in lex_response['slots']:
        # if lex_response['slots']['Direction'] == 'forward':
        polly_response = polly.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=lex_response['slots']['Direction'])
        if "AudioStream" in polly_response:
            output += 1
            file = open(str(output) + '.mp3', 'wb')
            file.write(polly_response['AudioStream'].read())
            file.close()
            play(str(output) + '.mp3')
    else:
        listen()


def play(file_name):
    mixer.music.load(file_name)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)
    listen()


listen()
