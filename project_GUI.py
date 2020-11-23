from time import ctime # get time details
import datetime
import webbrowser # open browser
import time
import requests, json 
import wolframalpha
import pyttsx3
import webbrowser
import azure.cognitiveservices.speech as speechsdk
import mysql.connector
from mysql.connector import errorcode
from tkinter import *
from PIL import ImageTk,Image
import sqlite3
from tkinter import messagebox
import webbrowser
import tkinter as tk
import sounddevice as sd
import soundfile as sf
from_language, to_languages = 'en-US', [ 'de', 'en', 'it', 'pt', 'zh-Hans' ]
speech_key, service_region = "61b8a438ab6e4afa8d7496ab6982d4e3", "eastus"

# Splash screen
def splash():
	sroot = Tk()
	sroot.geometry('450x400')
	sroot.title("Splash window")
	# Hide border
	sroot.overrideredirect(1)
	# Center splash window
	sroot.eval('tk::PlaceWindow . center')
	sroot.configure()
	img = Image.open("Logo.jpg")
	render = ImageTk.PhotoImage(img)
	img = Label(sroot, image = render)
	img.image = render
	img.place(x = -167, y = -60)

	def call_mainroot():
		sroot.destroy()
		mainroot()

	sroot.after(2500, call_mainroot)         #Time frame for splash screen

splash()

def mainroot():
    # Main screen
    root = Tk()
    root.geometry('350x500')
    root.configure(background='#F0F8FF')
    root.title('Rocket Voice Assistant')
    root.resizable(False, False)
    #root.overrideredirect(1)
    # # Text field and scroll bar
    t = Text(root, height = 31, width = 45, state = DISABLED)
    t.place(x = 13, y = 10)
    # Center main window
    root.eval('tk::PlaceWindow . center')

    # Popup window when closing the program
    def on_closing():
        if messagebox.askokcancel("Warning", "Do you want to quit the application?", icon = 'warning'):
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Function to open website
    new = 1
    url = "http://et791.ni.utoledo.edu/~ylu10/schedule/"
    
    def openweb():
        webbrowser.open(url, new = new)

    def start():
        speak("Hello, how may I help you")
        voice_data = record_audio()
        response = ai(voice_data)
        Skills(response)
        root.update()

    #listen for auio and convert it to text:
    def record_audio(ask=False):
        speech_key, service_region = "61b8a438ab6e4afa8d7496ab6982d4e3", "eastus"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            t.config(state = NORMAL)
            Response1 = "Recognized: {}\n".format(result.text)
            t.insert(tk.END, Response1)
            t.config(state = DISABLED)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
            t.config(state = NORMAL)
            Response2 = "No speech could be recognized: {}\n".format(result.no_match_details)
            t.insert(tk.END, Response2)
            t.config(state = DISABLED)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            t.config(state = NORMAL)
            Response3 = "Speech Recognition canceled: {}\n".format(cancellation_details.reason)
            t.insert(tk.END, Response3)
            t.config(state = DISABLED)
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                t.config(state = NORMAL)
                Response3 = "Error details: {}\n".format(cancellation_details.error_details)
                t.insert(tk.END, Response3)
                t.config(state = DISABLED)
        return result.text.lower()

        #get string and make a audio file to be played
    def speak(audio_string):
        speech_key, service_region = "61b8a438ab6e4afa8d7496ab6982d4e3", "eastus"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Creates a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        # Receives a text.
        text = audio_string

        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        result = speech_synthesizer.speak_text_async(text).get()

        # Checks result.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
            t.config(state = NORMAL)
            Response4 = f"Rocket: {audio_string}\n"
            t.insert(tk.END, Response4)
            t.config(state = DISABLED)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            print("Did you update the subscription info?")
        
    
    
    # This is the section of code which creates buttons
    Button(root, text='Start', bg='#FFFACD', font=('arial', 12, 'normal'),command = start, padx = 10, pady = 5, relief = GROOVE).place(x=25, y=440)
    Button(root, text='Quit', bg='#FFFACD', font=('arial', 12, 'normal'), command = on_closing, padx = 10, pady = 5, relief = GROOVE).place(x=107, y=440)
    Button(root, text='Class Schedule', bg='#FFFACD', font=('arial', 12, 'normal'), command = openweb, padx = 10, pady = 5, relief = GROOVE).place(x=185, y=440)

# End Of main window

    #LUIS
    def ai(voice_data):

        try:
        # Old app rocket @luis.ai
        
        #appId = '28efab5b-8c7e-49bd-8582-84d8152f792b'
        #prediction_key = '5c7fba2628cc498d985d95141263659c'
        #prediction_endpoint = 'https://rocket.cognitiveservices.azure.com/'
        
            appId = '28efab5b-8c7e-49bd-8582-84d8152f792b'
            prediction_key = '2851b2d126ce4c1d8f743632e0111e5a'
            prediction_endpoint = 'https://luisrva.cognitiveservices.azure.com/'


        # homeauto app @luis.ai
        #appId = '4b111d3b-e2b1-42a0-ab30-188c3fec9da2'
        #prediction_key = '4aaf3467a19d4df89151bf33cb76335e'
        #prediction_endpoint = 'https://westus.api.cognitive.microsoft.com/'


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
            x = response.json()
            print(x)
   
        except Exception as e:
            # Display the error string.
            print(f'{e}')

        return response.json()


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
            if int(value) > 0:
                cursor.execute("UPDATE devices SET value = value + %s WHERE name = %s;", (value, device))
                print("Updated",cursor.rowcount,"row(s) of data.")  

            else:
                value = -1*value
                cursor.execute("UPDATE devices SET value = value - %s WHERE name = %s;", (value, device))
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
        appid = "JHKVPE-RAH5E7T86Q"
        base_url = "http://api.wolframalpha.com/v1/conversation.jsp?appid="

        complete_url = base_url + appid + "&i=" + question

        response = requests.get(complete_url)
        x= response.json()
                
        print(x)

        return x

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


    def translate_speech_to_text():
        translation_config = speechsdk.translation.SpeechTranslationConfig(
                subscription=speech_key, region=service_region)

        translation_config.speech_recognition_language = from_language
        for lang in to_languages:
            translation_config.add_target_language(lang)

        recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=translation_config)
        
        print('Say something...')
        result = recognizer.recognize_once()
        synthesize_translations(result=result) 
        play_translation(result=result)


    def synthesize_translations(result):
        language_to_voice_map = {
            "de": "de-DE-KatjaNeural",
            "en": "en-US-AriaNeural",
            "it": "it-IT-ElsaNeural",
            "pt": "pt-BR-FranciscaNeural",
            "zh-Hans": "zh-CN-XiaoxiaoNeural"
        }
        print(f'Recognized: "{result.text}"')

        for language in result.translations:
            translation = result.translations[language]
            print(f'Translated into "{language}": {translation}')

            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            speech_config.speech_synthesis_voice_name = language_to_voice_map.get(language)
            
            audio_config = speechsdk.audio.AudioOutputConfig(filename=f'{language}-translation.wav')
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            speech_synthesizer.speak_text_async(translation).get()
        

    def play_translation(result):
            filename = "zh-Hans-translation.wav"
            data, fs = sf.read(filename, dtype='float32')  
            sd.play(data, fs)
            status = sd.wait() 
        

    def Skills(response):
        text = response["query"]
        response = response["prediction"]
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
        
        #translate
        elif (intent == "get_translation"):
            translate_speech_to_text()


        #
        elif (intent == "get_time"):
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)

        elif (intent == "get_answer"):
        
            x = wolframAlpha_API(text)
            
            if "error" in x:
                speak("Here is what I find in google")
                url = "http://www.google.com/search?btnG=1&q=%s"
                search = text
                webbrowser.open(url % search)
            else:
                speak(x["result"])

        elif (intent == "get_schedule"):
            day = first_entity(response['entities'], 'weekday')
            time = first_entity(response['entities'], 'time')
            print(day)
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

            if(day != None and time != None):
                if "pm" in time or "am" in time:
                    in_time = datetime.datetime.strptime(time, "%I:%M %p")
                    out_time = datetime.datetime.strftime(in_time, "%H:%M")
                    print(out_time)

                    cursor.execute("SELECT * FROM class where weekday="+ "'" + day + "' and start_time="+ "'" + out_time + "'" )
                    myresult = cursor.fetchall()
                    for row in myresult:
                        weekday = row[1]
                        start = row[2]
                        end = row[3]
                        course = row[4]
                        speak("You have " + course + " class on " + weekday + " at " + start +" to " + end)
                
                if not myresult:
                    speak("You don't have class on " + day + " at " + out_time + " but")
                    cursor.execute("SELECT * FROM class where weekday="+ "'" + day + "'")
                    myresult = cursor.fetchall()
                    for row in myresult:
                        weekday = row[1]
                        start = row[2]
                        end = row[3]
                        course = row[4]
                    speak("You have " + course + " class on " + weekday + " at " + start +" to " + end)
            else:
                if(day == None):
                    today = datetime.date.today()
                    day = today.strftime("%A")

                if(day == "tomorrow"):
                    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                    day = tomorrow.strftime("%A")
            
            
                cursor.execute("SELECT * FROM class where weekday="+ "'" + day + "'")
                myresult = cursor.fetchall()
                print(myresult)
                #print(myresult[0])
                if not myresult:
                    speak("You don't have class on " + day)
                for row in myresult:
                    weekday = row[1]
                    start = row[2]
                    end = row[3]
                    course = row[4]

                    speak("You have " + course + " class on " + weekday + " at " + start +" to " + end)

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
            value = int(get_value(response))
            update_db(device=device, value=-1*value)
            speak("Turning down the {} by {} degrees".format(device, value))
        
        elif (intent == "goodbye"):
            speak("Take care")
            exit()

        elif (intent == None):
            speak("I didn't understand that. Could you repeat the question?")

    
    root.mainloop()

mainloop()
