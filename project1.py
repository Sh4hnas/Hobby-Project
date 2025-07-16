import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes
import os
import google.generativeai as genai


def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            print("You said:", data)
            return data.lower()
        except sr.UnknownValueError:
            print("Not Understanding!!!")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None

def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(x)
    engine.runAndWait()

def ai_chat(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, I couldn't answer that."


genai.configure(api_key="AIzaSyDuiSDzAGgxX8aMW-4wHExWls2CVIs1kec")

model = genai.GenerativeModel(model_name="models/gemini-pro")  

def ai_chat(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry, I couldn't answer that."


if __name__ == '__main__':
    while True:
        data1 = sptext()
        if data1 is not None:
            if "your name" in data1:
                speechtx("My name is ALEXA")

            elif "age" in data1:
                speechtx("I am 4 years old")

            elif "time" in data1:
                time = datetime.datetime.now().strftime("%I:%M %p")
                speechtx("Current time is " + time)

            elif "youtube" in data1:
                webbrowser.open("https://www.youtube.com/")
                speechtx("Opening YouTube")

            elif "joke" in data1:
                joke = pyjokes.get_joke(language='en', category='neutral')
                print(joke)
                speechtx(joke)

            elif "song" in data1:
                try:
                    add = r'C:\Users\rahim\Desktop\songs'
                    songs = os.listdir(add)
                    os.startfile(os.path.join(add, songs[0]))
                    speechtx("Playing song")
                except Exception as e:
                    print("Song error:", e)
                    speechtx("Sorry, I couldn't play the song.")

            elif "exit" in data1 or "quit" in data1:
                speechtx("Goodbye!")
                break

            else:
                response = ai_chat(data1)
                print("AI:", response)
                speechtx(response)
