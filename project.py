import speech_recognition as sr # recognise speech
import playsound # to play an audio file
#from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import datetime
import webbrowser # open browser
#import yfinance as yf # to fetch financial data
import ssl
import certifi
import time
import os # to remove created audio files
from wit import Wit
import requests, json 
#import wolframalpha
import pyttsx3
import wikipedia
import webbrowser
import azure.cognitiveservices.speech as speechsdk
import mysql.connector
from mysql.connector import errorcode

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

#initialise a recogniser
r = sr.Recognizer()

#listen for auio and convert it to text:
def record_audio(ask=False):
    speech_key, service_region = "61b8a438ab6e4afa8d7496ab6982d4e3", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    result = speech_recognizer.recognize_once()


    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    
    return result.text.lower()


#get string and make a audio file to be played
def speak(audio_string):
#   tts = gTTS(text=audio_string, lang='en') #text to speech    
#    audio_file = 'audio' + '.mp3'
#    tts.save(audio_file) # save as mp3
#    playsound.playsound(audio_file) # play the audio file
#    print(f"Rocket: {audio_string}") # print what app said
#    os.remove(audio_file) # remove audio file
    engine = pyttsx3.init()
    engine.say(audio_string)
    print(f"Rocket: {audio_string}")
    engine.runAndWait()

#WIT.AI
def ai(voice_data):
    access_token = "4QKSOGCQXLBPF6LHFD2R4YRETJ24NF5H"
    client = Wit(access_token = access_token)
    response = client.message(voice_data)
    print(response)
    return response  

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]
    if not val:
        return None
    return val

def first_entity_resolved_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]
    if 'resolved' not in val:
        return None
    val = val['resolved']['values'][0]
    if not val:
        return None
    return val


def first_trait_value(traits, trait):
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val

#WolframAlpha API
def wolframAlpha_API (question):
    app_id="JHKVPE-RAH5E7T86Q"
    client = wolframalpha.Client('R2K75H-7ELALHR35X')
    res = client.query(question)
    answer = next(res.results).text

    return answer


#Weather API
#convert Kelvin to Fahrenheit
def convert (t):
    f =  int((t - 273.15)* 1.8 + 32)
    return f

def weather_API (city_name):  
    #API Key
    api_key = "5b1d106830d353e715394db3889c0eaf"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + ",US"
    
    # return response object 
    response = requests.get(complete_url) 

    x = response.json() 

    if x["cod"] != "404": 
    
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        #Temperature (in kelvin unit)
        current_temperature = convert(y["temp"])
        max_temperature = convert(y["temp_max"])
        min_temperature = convert(y["temp_min"])
    
        # store the value of "weather" 
        z = x["weather"] 
    
        # to the "description" key at  
        weather_description = z[0]["description"] 
    
    else: 
        print(" City Not Found ") 
        return "City not found"
    
    p = "Right now in " + city_name + " the temperature is " + str(current_temperature) + " fahrenheit with " + weather_description + " higher " + str(max_temperature) + " degree and lower " + str(min_temperature) +" degree"
    return p

    

def Skills(response):
    print('response is ', response)
    y = response["intents"]
    intent = y[0]["name"]
    print("intent is " + intent)

#trait = first_trait_value(response['traits'], 'wit$greetings')
#entity = first_entity_resolved_value(response['entities'], 'wit$notable_person:notable_person')
# intent stands for the action that a user wants to perform, e.g., show the weather. 
# Entities clarify the characteristics of a given intent, e.g., the time and place of a user
   
    #
    if (intent == "weather"):
        entity = first_entity_resolved_value(response['entities'], 'wit$location:location')
        print("print(entity)", entity)
        if (entity == None):
            speak("What is the city name")
            response = ai(record_audio())
            entity = first_entity_resolved_value(response['entities'], 'wit$location:location')["name"]
            print("print(entity)", entity)
            speak(weather_API(entity))
        else:
            entity = first_entity_resolved_value(response['entities'], 'wit$location:location')["name"]
            speak(weather_API(entity))

    #
    elif (intent == "math"):
        entity = first_entity_value(response['entities'], 'wit$math_expression:math_expression')["body"]
        print(entity)
        speak(entity + " = " + wolframAlpha_API(entity))

    #
    elif (intent == "time"):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(strTime)

    #
    elif (intent == "wikipedia"):
        statement =  first_entity_value(response['entities'], 'wit$wikipedia_search_query:wikipedia_search_query')["body"]
 
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia " + results)

    #
    elif (intent == "search"):
        statement = first_entity_value(response['entities'])

        print(response['text'])

    #
    # speak("I am rockets. I created by UT student. ")
    # speak("My favorite color is yellow and blue.")


    elif (intent == "get_schedule"):
        d = first_entity_value(response['entities'], 'wit_date:wit_date')["body"]
        time = first_entity_value(response['entities'], 'wit_time:wit_time')["body"]
        print(d)
        print(time)

        config = {
        'host':'rvaschedule.mysql.database.azure.com',
        'user':'rvaschedule@rvaschedule',
        'password':'RVA2020!',
        'database':'rocket'
        }

        # Construct connection string
        try:
            conn = mysql.connector.connect(**config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor = conn.cursor()

        cursor.execute("SELECT * FROM class where weekday="+ "'" + d+ "'")
        myresult = cursor.fetchall()
        print(myresult)
        for row in myresult:
            day = row[1]
            start = row[2]
            end = row[3]
            course = row[4]
              
        speak("You have " + course + " class on " + day + " at " + str(start))
       

    #
    elif (intent == "goodbye"):
        speak("Take care")
        exit()


speak("Hello, how may I help you")
while(1):
    
    voice_data = record_audio()
    response = ai(voice_data)
    Skills(response)
