import speech_recognition as sr
import pyttsx3
import webbrowser
from langdetect import detect, DetectorFactory
import wikipediaapi
import datetime
from googletrans import Translator



DetectorFactory.seed=0
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator=Translator()
voices = engine.getProperty('voices')

for voice in voices:
    if "female" in voice.name.lower():  # Look for a voice with "female" in the name
        engine.setProperty('voice', voice.id)
        break
else:
    engine.setProperty('voice', voices[1].id)  # Default to the second voice if no female is found

engine.setProperty('rate', 170)
def speak(text, lang="en"):
    """Convert text to speech and translate if needed."""
    if lang != "en":
        translated_text = translator.translate(text, dest=lang).text
    else:
        translated_text = text

    print(f"Speaking: {translated_text}")
    engine.say(translated_text)
    engine.runAndWait()

def get_time():
    """Get the current time and speak it."""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %P")  # Format: HH:MM AM/PM
    speak(f"The time is {current_time}")
    print(f"The time is {current_time}")


    
def get_biodata(person):
    """Fetch biodata from Wikipedia."""
    try:
        speak("searching for biodata")
        result=wikipediaapi.summary(person,sentences=2)
        print(result)
        speak(result)
    except wikipediaapi.exceptions.PageError:
        print("sorry,i could not found the information about the topic you had given ")
    except wikipediaapi.exceptions.DisambiguationError as e:
        print("there are so many data's, can you be more specifc")
        print("possible options",e.options)

def detect_language(text):
    try:
        lang=detect(text)
    except:
        return"unknown"


commands = {
         "google":("open google","google khol",),
         "youtube":("open youtube","youtube khol",),
         "wikipedia":("open wikipedia","wikipedia khol",),
         "chatgpt": ("open chatgpt", "chatgpt khol"),
         "gemini": ("open gemini", "open bard"),
         "copilot": ("open copilot", "open microsoft ai"),
         "perplexity": ("open perplexity ai",),
     }

def process_command(c):
     c= c.lower()
     for key, phrases in commands.items():
        if any(phrase in c for phrase in phrases):
            webbrowser.open(f"https://{key}.com")

     if any(cmd in c for cmd in commands["google"]):
        webbrowser.open("https://google.com")
     elif any(cmd in c for cmd in commands["youtube"]):
        webbrowser.open("https://youtube.com")
     elif any(cmd in c for cmd in commands["wikipedia"]):
        webbrowser.open("https://wikipedia.com")
     elif any(cmd in c for cmd in commands["chatgpt"]):
        webbrowser.open("https://chat.openai.com")
     elif "who is" in c or "biodata of" in c:
        person = c.replace("who is", "").replace("biodata of", "").strip()
        get_biodata(person)

     elif "open chatgpt" in c:
        speak("Opening ChatGPT...")
        webbrowser.open("https://chat.openai.com")
     elif "open gemini" in c or "open bard" in c:
        speak("Opening Gemini AI...")
        webbrowser.open("https://gemini.google.com")
     elif "open copilot" in c or "open microsoft ai" in c:
        speak("Opening Microsoft Copilot...")
        webbrowser.open("https://copilot.microsoft.com")
     elif "open perplexity ai" in c:
        speak("Opening Perplexity AI...")
        webbrowser.open("https://www.perplexity.ai")
   
     elif c in ["stop", "exit", "shutdown", "bye"]:
        speak("Goodbye! Shutting down...")
        exit()  


     else:
         speak("command not recognized")


if __name__ == "__main__":
    wake_word="david"
    speak("Initializing...")

    while True:
        print("Listening for wake word 'david'...")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
                print('Listening...')
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
                word = recognizer.recognize_google(audio).lower()

            if word == wake_word:
                speak("Yes, how can I assist you?")
                print("david activated...")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio).lower()
                
                process_command(command)  # Call function only if a command is received
        
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Could not request results, check your internet connection")
        except Exception as e:
            print(f"Error: {e}")
