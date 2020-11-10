import speech_recognition as sr # recognise speech
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import datetime
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files
from wit import Wit
import requests, json 
import wolframalpha
import pyttsx3
import wikipedia
import webbrowser
import azure.cognitiveservices.speech as speechsdk
import mysql.connector
from mysql.connector import errorcode

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
    engine = pyttsx3.init()
    engine.say(audio_string)
    print(f"Rocket: {audio_string}")
    engine.runAndWait()

#LUIS
def ai(voice_data):

    try:
        # @luis.ai
        """
        appId = '28efab5b-8c7e-49bd-8582-84d8152f792b'
        prediction_key = '5c7fba2628cc498d985d95141263659c'
        prediction_endpoint = 'https://rocket.cognitiveservices.azure.com/'       
        """
        appId = '28efab5b-8c7e-49bd-8582-84d8152f792b'
        prediction_key = '2851b2d126ce4c1d8f743632e0111e5a'
        prediction_endpoint = 'https://luisrva.cognitiveservices.azure.com/'

        """
        # homeauto app @luis.ai
        appId = '4b111d3b-e2b1-42a0-ab30-188c3fec9da2'
        prediction_key = '4aaf3467a19d4df89151bf33cb76335e'
        prediction_endpoint = 'https://westus.api.cognitive.microsoft.com/'
        """

        # The utterance you want to use.
        utterance = voice_data

        # The headers to use in this REST call.
        headers = {
        }

        # The URL parameters to use in this REST call.
        params ={
            'query': utterance,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': prediction_key
        }

        # Make the REST call.
        response = requests.get(f'{prediction_endpoint}luis/prediction/v3.0/apps/{appId}/slots/production/predict', headers=headers, params=params)
        #response = requests.get(f'{prediction_endpoint}luis/prediction/v3.0/apps/{appId}/slots/production/predict', headers=headers, params=params)
        
        # Display the results on the console.
        x = response.json()["prediction"]
        print(x)
   
    except Exception as e:
        # Display the error string.
        print(f'{e}')

    return response.json()["prediction"]


def first_entity(entities, entity, querystate=False):
    if entity not in entities:
        ent = None
    elif querystate == True:
        ent = entities[entity][1]
    else:
        ent = entities[entity][0]

    return ent


def get_value(response):
    return first_entity(response['entities'], 'HomeAutomation.NumericalChange')


def update_db(device, state=None, value=None):

    config = {
        'host':'rva-server.mysql.database.azure.com',
        'user':'rvaadmin@rva-server',
        'password':'Faisal1996?',
        'database':'homeautodb'
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
            print("some other error : ", err)
    else:
        cursor = conn.cursor()
        print("connected") 

    # Update a data row in the table
    if state is not None:
        # update state
        cursor.execute("UPDATE devices SET state = %s WHERE name = %s;", (state, device))
        print("Updated",cursor.rowcount,"row(s) of data.")
    
    if value is not None:
        # update state
        cursor.execute("UPDATE devices SET value = value + %s WHERE name = %s;", (value, device))
        print("Updated",cursor.rowcount,"row(s) of data.")       

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")


def query_db(device):

    config = {
        'host':'rva-server.mysql.database.azure.com',
        'user':'rvaadmin@rva-server',
        'password':'Faisal1996?',
        'database':'homeautodb'
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
            print("some other error : ", err)
    else:
        cursor = conn.cursor()
        print("connected")

    # Read data
    cursor.execute("SELECT * FROM devices;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")

    # Print all rows
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))
        if row[0]==device:
            return {'state':row[1], 'value':row[2]}
      
    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")


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
    if response is None:
        speak("It was not clear. Please try again")
        exit()
    else:
        intent = response["topIntent"]
    

#trait = first_trait_value(response['traits'], 'wit$greetings')
#entity = first_entity_resolved_value(response['entities'], 'wit$notable_person:notable_person')
# intent stands for the action that a user wants to perform, e.g., show the weather. 
# Entities clarify the characteristics of a given intent, e.g., the time and place of a user
   
    #
    if (intent == "get_weather"):
        entity = first_entity(response["entities"], 'location')
        print("print(entity)", entity)
        if (entity == None):
            speak("What is the city name")
            response = ai(record_audio())
            entity = first_entity(response['entities'], 'location')
            print("print(entity)", entity)
            speak(weather_API(entity))
        else:
            #entity = first_entity_resolved_value(response['entities'], 'wit$location:location')["name"]
            speak(weather_API(entity))

    
    #elif (intent == "math"):
       
    
    #
    elif (intent == "get_time"):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(strTime)

    
    #elif (intent == "wikipedia"):
        

    
    #elif (intent == "search"):
        

    #
    # speak("I am rockets. I created by UT student. ")
    # speak("My favorite color is yellow and blue.")

    elif (intent == "get_schedule"):
        d = first_entity(response['entities'], 'weekday')
        time = first_entity(response['entities'], 'time')
        print(d)
        print(time)

        # Connect database
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
        print(myresult[0])
        if(myresult[0][1] == ""):
            speak("You don't have class on " + d)
        for row in myresult:
            day = row[1]
            start = row[2]
            end = row[3]
            course = row[4]
              
            speak("You have " + course + " class on " + day + " at " + str(start))

    elif (intent == "HomeAutomation.QueryState"):

        if next(iter(response['entities']))=='HomeAutomation.DeviceType':
            # this True parameter is to solve the coffee maker problem in the model
            device = first_entity(response['entities'], 'HomeAutomation.DeviceType', True)[0]
            if query_db(device)['state']==1:
                #device is on
                speak(device + " is on")
            else:
                speak(device + " is off")
        
        elif next(iter(response['entities']))=='HomeAutomation.Location' or next(iter(response['entities']))=='HomeAutomation.SettingType':
            # this True parameter is to solve the coffee maker problem in the model
            device = 'ac'
            speak('room temperature is {} degrees'.format(query_db('ac')['value']))

    # intent is not a query state
    elif (intent == "HomeAutomation.TurnOff"):

        #turning off the device and update it in the database
        device = first_entity(response['entities'], 'HomeAutomation.DeviceType')[0]
        update_db(device=device, state='0')
        speak("Turning off the "+ device)

    elif (intent == "HomeAutomation.TurnOn"):

        #turning on the device and update it in the database
        device = first_entity(response['entities'], 'HomeAutomation.DeviceType')[0]
        update_db(device=device, state="1")
        speak("Turning on the "+ device)

    elif (intent == "HomeAutomation.TurnUp"):

        #turning up the settings and update it in the database
        device = first_entity(response['entities'], 'HomeAutomation.DeviceType')[0]
        value = get_value(response)
        update_db(device=device, value=value)
        speak("Turning up the {} by {} degrees".format(device, value))

    elif (intent == "HomeAutomation.TurnDown"):

        #turning down the settings and update it in the database
        device = first_entity(response['entities'], 'HomeAutomation.DeviceType')[0]
        value = get_value(response)
        update_db(device=device, value=value)
        speak("Turning down the {} by {} degrees".format(device, (-1)*value))

    elif (intent == "goodbye"):
        speak("Take care")
        exit()

    speak("Do you need any other help")


speak("Hello, how may I help you")
while(1):
    
    voice_data = record_audio()
    response = ai(voice_data)
    Skills(response)

"""

#voice_data = 'turn the ac to 30 degree'
#voice_data = 'increase the ac by 10 degrees'
voice_data = 'what is the room temperature'
#voice_data = 'what is weather?'
#voice_data = 'what class do i have on wednesday'
response = ai(voice_data)
Skills(response)
"""
