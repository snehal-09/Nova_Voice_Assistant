
import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil
import subprocess
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query,
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Snehal, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Snehal, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Snehal, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()

    GREETING = "Hey Snehal"
    speak(f"{GREETING}, here’s your schedule for today.")

    week = {
        "monday": (
            "Today focuses on building your core foundations. "
            "From 9:00 to 9:50 you have Algorithms class, sharpening your problem-solving skills. "
            "From 10:00 to 11:50 you have System Design class, essential for scalable AI systems. "
            "From 12:00 to 2:00 you have a break. "
            "From 2:00 onwards, you have Programming Lab to strengthen your coding practice."
        ),

        "tuesday": (
            "Today is about practical development and data handling. "
            "From 9:00 to 9:50 you have Web Development class. "
            "From 10:00 to 10:50 you have a short break. "
            "From 11:00 to 12:50 you have Database Systems class, important for managing AI data. "
            "From 1:00 to 2:00 you have a break. "
            "From 2:00 onwards, you have Open Source Projects lab to gain real-world experience."
        ),

        "wednesday": (
            "Today is a heavy learning day focused on intelligence and systems. "
            "From 9:00 to 10:50 you have Machine Learning class. "
            "From 11:00 to 11:50 you have Operating Systems class. "
            "From 12:00 to 12:50 you have Ethics in Technology class, essential for responsible AI. "
            "From 1:00 to 2:00 you have a break. "
            "From 2:00 onwards, you have a Software Engineering workshop."
        ),

        "thursday": (
            "Today strengthens your understanding of networks and cloud platforms. "
            "From 9:00 to 10:50 you have Computer Networks class. "
            "From 11:00 to 12:50 you have Cloud Computing class, important for deploying AI models. "
            "From 1:00 to 2:00 you have a break. "
            "From 2:00 onwards, you have Cybersecurity lab."
        ),

        "friday": (
            "Today blends intelligence, creativity, and advanced coding. "
            "From 9:00 to 9:50 you have Artificial Intelligence class. "
            "From 10:00 to 10:50 you have Advanced Programming class. "
            "From 11:00 to 12:50 you have UI/UX Design class. "
            "From 1:00 to 2:00 you have a break. "
            "From 2:00 onwards, you work on your Capstone Project."
        ),

        "saturday": (
            "Today is lighter but productive. "
            "From 9:00 to 11:50 you have Capstone Project team meetings. "
            "From 12:00 to 12:50 you have Innovation and Entrepreneurship class. "
            "From 1:00 to 2:00 you have a break. "
            "From 2:00 onwards, you focus on personal development, AI practice, and coding."
        ),

        "sunday": (
            "Today is a rest and reflection day. "
            "Use this time to revise concepts, work on personal AI projects, "
            "practice coding, and prepare for upcoming goals."
        )
    }

    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("Boss, what should i search on google..")
        s = command().lower()
        webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Snehal our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Snehal we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Snehal we should connect our system to charging point to charge our battery")
    else:
        speak("Snehal we have very low power, please connect to charging otherwise recording should be off...")

if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Jarvis...")

    while True:
        # Use ONLY ONE input method (text input for now)
        query = command().lower()
        #query = input("Enter your command-> ").lower()

        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)

        elif ("university time table" in query) or ("schedule" in query):
            schedule()

        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")

        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")

        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")

        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)

        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)

        elif ("open google" in query) or ("open edge" in query):
            browsing(query)

        elif ("system condition" in query) or ("condition of the system" in query):
            speak("Checking the system condition")
            condition()

        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(
                tokenizer.texts_to_sequences([query]),
                maxlen=20,
                truncating='post'
            )
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))

        elif "exit" in query:
            speak("Goodbye Snehal")
            sys.exit()
