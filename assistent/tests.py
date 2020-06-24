import json

with open('credentials/weather-credentials.json','r') as weather_credentials:
        WEATHER_API_CREDENTIALS = json.load(weather_credentials)['apiKey']

print(WEATHER_API_CREDENTIALS)