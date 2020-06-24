import speech_recognition as sr
from playsound import playsound
from gtts import  gTTS
from bs4 import BeautifulSoup
import requests
import os
import webbrowser as browser
import json
import sys


with open('assistent/credentials/weather-credentials.json','r') as weather_credentials:
    WEATHER_API_CREDENTIALS = json.load(weather_credentials)['apiKey'] 


def execute_audio(text:str, filename:str):

    tts = gTTS(text, lang='en')
    audio_path = f'assistent/audios/{filename}.mp3'
    tts.save(audio_path)
    playsound(audio_path)
    os.unlink(audio_path)


class News:

    def __init__(self, next_command):

        self.__next_command = next_command

    def execute_command(self, trigger):
    
        if 'news' in trigger:
                
            news_br = 'https://news.google.com/rss?gl=BR&hl=pt-BR&ceid=BR:pt-419'
            site = requests.get('https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en')
            news = BeautifulSoup(site.text,'html.parser')

            for counter, item in enumerate(news.findAll('item')[:5]):
                message = item.title.text.split('-')
                message = f'from {message[1]}: {message[0]}'
                
                execute_audio(text=message,filename=f'message')
        else:
            self.__next_command.execute_command(trigger)

class Playlist:

    def __init__(self, next_command):

        self.__next_command = next_command
    
    def execute_command(self, trigger):

        if 'play' in trigger and 'first album' in trigger:
            browser.open('https://open.spotify.com/track/1f3lBHYLr6EhKW8bv7YIxo?\
                    si=dUrrKD8zQpG7cFd0Myd_KQ')
        else:
            self.__next_command.execute_command(trigger)

class Weather:

    def __init__(self, next_command):

        self.__next_command = next_command

    def execute_command(self, trigger, weather=False, minmax=False):
        
        if 'weather' in trigger:
            weather = True
        elif 'temperature' in trigger:
            minmax = True

        if weather or minmax:

            site = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q=fortaleza,br\
                &appid={WEATHER_API_CREDENTIALS}&units=metric')
            weather = site.json()
            temperature = weather['main']['temp']
            temp_min = weather['main']['temp_min']
            temp_max = weather['main']['temp_max']
            description = weather['weather'][0]['description']

            if weather:
                message = f'At the moment in Fortaleza it is {temperature} degrees with: {description}'
            if minmax:
                message = f'Minimum of {temp_min} and maximum of {temp_max}' 

            execute_audio(text=message, filename='weather')
            return message, 'message' 

        else:
            self.__next_command.execute_command(trigger)


class AssistentExit:

    def execute_command(self, trigger):

        if 'bye' in trigger:
            execute_audio(text="bye bye", filename='bye')
            sys.exit()  

    
def commands_chain(trigger:str):

    command = News(
                Playlist(
                    Weather(
                        AssistentExit()   
                    )
                )
            ).execute_command(trigger=trigger)

