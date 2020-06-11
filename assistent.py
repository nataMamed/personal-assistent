import speech_recognition as sr
from playsound import playsound

### CONFIGURATIONS ###
hotword = 'nathan'

with open('credentials/credentials.json', 'r') as google_credentials:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = google_credentials.read()

### MAIN FUNCTIONS ###
def monitors_audio():

    microphone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Waiting for a command...")
            audio = microphone.listen(source)
            try:
                trigger = microphone.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='en')
                trigger = trigger.lower()
                if hotword in trigger:
                    print("Command: ", trigger)
                    awnser('feedback')
                    break

            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return trigger

def awnser(filename):

    audio_path = f'audios/{filename}.mp3'
    playsound(audio_path)

def main():
    monitors_audio()

if __name__=='__main__':
    main()