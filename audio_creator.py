from gtts import  gTTS
#from subprocess import call
from playsound import playsound

def create_audio(audio:str, filename:str):

    tts = gTTS(audio, lang='en')
    audio_path = f'audios/{filename}.mp3'
    tts.save(audio_path)
    # call(['afplay', 'audios/hello.mp3']) # MacOSX
    # call(['aplay', 'audios/hello.mp3']) # Linux
    playsound(audio_path) #Windows

if __name__=='__main__':
    create_audio('Wait my friend', 'feedback')