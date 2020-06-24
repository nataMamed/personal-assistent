import speech_recognition as sr
from playsound import playsound
from gtts import  gTTS
import requests
import os
import json
from commands import commands_chain


### CONFIGURATIONS ###
HOTWORD = 'alexis'

with open('assistent/credentials/google-credentials.json', 'r') as google_credentials:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = google_credentials.read()

### MAIN FUNCTIONS ###
def monitors_audio():

    microphone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Waiting for a command...")
            audio = microphone.listen(source)
            try:
                trigger = microphone.recognize_google_cloud(audio, 
                credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='en')

                if verifies_hotword(trigger):
                    commands_chain(trigger=trigger)
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google\
                     Cloud Speech service; {0}".format(e))

    return trigger

### VERIFICATIONS ##
def verifies_hotword(trigger:str) -> bool:

    trigger = trigger.lower()
    if HOTWORD in trigger:
        print("COMMAND: ", trigger)
        awnser('feedback')
        return True
    return 

### EXECUTABLES ###
def awnser(filename:str):

    audio_path = f'assistent/audios/{filename}.mp3'
    playsound(audio_path)


def create_audio(text:str, filename:str):

    tts = gTTS(text, lang='en')
    audio_path = f'assistent/audios/{filename}.mp3'
    tts.save(audio_path)
    playsound(audio_path)
    os.unlink(audio_path)


### MAIN ###
def main():
    while True:
        monitors_audio()

main()
