# ================== IMPORTS ==================
import logging
logging.disable(logging.CRITICAL)

import speech_recognition as sr
import pywhatkit
import os
import pyautogui as pg
import time
import cv2
import numpy as np
from datetime import datetime
from openai import OpenAI
import pyttsx3
import wikipedia
import webbrowser
# import pyaudio
# ===================other new modules=============
import psutil
import pyperclip
import socket


# ================== FIX LOGGING ==================
logging.getLogger('comtypes').setLevel(logging.CRITICAL)

# ================== OPENAI ==================
client = OpenAI(
    api_key="YOUR_API_KEY_HERE"
)

# ================== VOICE ENGINE ==================
engine = pyttsx3.init(driverName="sapi5")

engine.setProperty("rate", 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ================== LISTEN ==================
def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except Exception as e:
        print("Mic error:", e)
        return None

# ================== AI CHAT ==================
def ai_chat(query):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=query
    )
    return response.output_text

# ================== SCREEN RECORD ==================
recording = False
video_writer = None

def start_recording():
    global recording, video_writer
    screen_size = pg.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter("screen_record.avi", fourcc, 8, screen_size)
    recording = True
    speak("Screen recording started")

def stop_recording():
    global recording, video_writer
    recording = False
    if video_writer:
        video_writer.release()
    speak("Screen recording saved")

def record_screen():
    if recording:
        img = pg.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        video_writer.write(frame)

# ================== FILE AUTOMATION ==================
def create_folder(name):
    os.makedirs(name, exist_ok=True)
    speak(f"Folder {name} created")

def create_file(name):
    with open(name, "w") as f:
        f.write("")
    speak(f"File {name} created")

def delete_path(name):
    if os.path.isfile(name):
        os.remove(name)
        speak("File deleted")
    elif os.path.isdir(name):
        os.rmdir(name)
        speak("Folder deleted")
    else:
        speak("File or folder not found")

def list_files(path="."):
    files = os.listdir(path)
    if not files:
        speak("Folder is empty")
    for f in files[:5]:
        speak(f)

# ================== CLIPBOARD ==================
def read_clipboard():
    text = pyperclip.paste()
    if text:
        speak("Clipboard contains")
        speak(text[:300])
    else:
        speak("Clipboard is empty")

# ================== SYSTEM INFO ==================
def system_info():
    battery = psutil.sensors_battery()
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"Battery {battery.percent} percent")
    speak(f"CPU usage {cpu} percent")
    speak(f"RAM usage {ram} percent")

def internet_status():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        speak("Internet is connected")
    except:
        speak("Internet is not connected")

# ================== NOTES ==================
def save_note(text):
    with open("jarvis_notes.txt", "a") as f:
        f.write(f"{datetime.now()} : {text}\n")
    speak("Note saved")

def read_notes():
    if os.path.exists("jarvis_notes.txt"):
        with open("jarvis_notes.txt") as f:
            speak(f.read())
    else:
        speak("No notes found")
 

# ================== WINDOW CONTROL ==================
def close_window():
    pg.hotkey("alt", "f4")
    speak("Closing current window")

# ================== START ==================
speak("Jarvis activated")

while True:
    record_screen()

    command = take_command()
    if not command:
        continue

    # ---------- AI ----------
    if "jarvis" in command or "question" in command:
        query = command.replace("jarvis", "").replace("question", "")
        speak(ai_chat(query))

    # ---------- WINDOW ----------
    elif "close window" in command or "close app" in command:
        close_window()

    elif "minimize window" in command:
        pg.hotkey("win", "down")
        speak("Window minimized")

    elif "maximize window" in command:
        pg.hotkey("win", "up")
        speak("Window maximized")

    elif "switch window" in command:
        pg.hotkey("alt", "tab")
        speak("Switching window")

    # ---------- SCREEN RECORD ----------
    elif "start recording" in command:
        start_recording()

    elif "stop recording" in command:
        stop_recording()

    # ---------- APPS ----------
    elif "open chrome" in command:
        os.system("start chrome")
        speak("Opening Chrome")

    elif "open vscode" in command or "open visual studio code" in command:
        os.system("code")
        speak("Opening Visual Studio Code")

    elif "open notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")

    # elif "open whatsapp" in command:
    #    os.system("start whatsapp:")
    #    speak("Opening WhatsApp")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp")

  

    elif "open calculator" in command:
        os.system("calc")
        speak("Opening Calculator")

    elif "open command prompt" in command:
        os.system("start cmd")
        speak("Opening Command Prompt")

    # ---------- WEB ----------
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "search" in command:
        q = command.replace("search", "")
        pywhatkit.search(q)
        speak(f"Searching {q}")

    # ---------- MEDIA ----------
    elif "play" in command and "youtube" in command:
        song = command.replace("play", "").replace("on youtube", "")
        pywhatkit.playonyt(song)
        speak(f"Playing {song}")

    elif "pause" in command:
        pg.press("playpause")

    # ---------- VOLUME ----------
    elif "volume up" in command:
        pg.press("volumeup")

    elif "volume down" in command:
        pg.press("volumedown")

    elif "mute" in command:
        pg.press("volumemute")

    # ---------- SYSTEM ----------
    elif "lock laptop" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("Laptop locked")

    elif "shutdown laptop" in command:
        speak("Shutting down laptop")
        os.system("shutdown /s /t 5")
        break

    elif "restart laptop" in command:
        speak("Restarting laptop")
        os.system("shutdown /r /t 5")
        break

    elif "sleep laptop" in command:
        speak("Laptop going to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    # ---------- UTILITIES ----------
    elif "take screenshot" in command:
        pg.screenshot(f"screenshot_{int(time.time())}.png")
        speak("Screenshot taken")

    elif "time" in command:
        speak(datetime.now().strftime("%I:%M %p"))

    elif "date" in command:
        speak(datetime.now().strftime("%d %B %Y"))

    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "")
        speak(wikipedia.summary(topic, sentences=2))

    # ---------- GREET ----------
    elif "hello" in command or "hi jarvis" in command:
        speak("Hello! How can I help you?")

    elif "how are you" in command:
        speak("I'm doing great and ready to help.")

    elif "thank you" in command:
        speak("You're welcome.")

    # ---------- EXIT ----------
    elif "stop jarvis" in command or "exit jarvis" in command:
        speak("Goodbye Tohid")
        break

#================File Commands================
    elif "create folder" in command:
       speak("Folder name?")
       create_folder(take_command())
  
    elif "create file" in command:
       speak("File name?")
       create_file(take_command())

    elif "delete file" in command or "delete folder" in command:
       speak("Name?")
       delete_path(take_command())

    elif "list files" in command:
       list_files()

# =================Clipboard Commands==============
    elif "copy" in command:
       pg.hotkey("ctrl", "c")
       speak("Copied")

    elif "paste" in command:
       pg.hotkey("ctrl", "v")
       speak("Pasted")

    elif "read clipboard" in command:
       read_clipboard()

# ================Browser Shortcuts===============
    elif "open gmail" in command:
       webbrowser.open("https://mail.google.com")
       speak("Opening Gmail")

    elif "open maps" in command:
       webbrowser.open("https://maps.google.com")
       speak("Opening Google Maps")

    elif "open website" in command:
       speak("Website name?")
       site = take_command().replace(" ", "")
       webbrowser.open(f"https://{site}.com")
       speak("Opening website")

    elif "search youtube" in command:
       q = command.replace("search youtube", "")
       webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
       speak("Searching YouTube")

# ===================Productivity=================
    elif "make note" in command:
       speak("What should I note?")
       save_note(take_command())

    elif "read notes" in command:
       read_notes()

    elif "set alarm" in command:
       speak("Say time in seconds")
       t = int(take_command())
       time.sleep(t)
       speak("Alarm ringing")

#=================System Info==================
    elif "system status" in command:
       system_info()

    elif "internet status" in command:
       internet_status()
    

    # ---------- FALLBACK ----------
    else:
        try:
            speak(ai_chat(command))
        except:
            speak("Sorry, I couldn't process that.")
