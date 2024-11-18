import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import time

# Initialization
#print('Loading your AI GENERAL ASSISTANT - BAY MAX')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Fixed setting voice ID


def speak(text):
    """Speak the given text using the text-to-speech engine."""
    engine.say(text)
    engine.runAndWait()


def wish_me():
    """Wish the user based on the current time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning!")
    elif 12 <= hour < 18:
        speak("Hello, Good Afternoon!")
    else:
        speak("Hello, Good Evening!")


def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

# if you want to give the text as input you can uncomment the following code
# def take_command():
#     """Take user input from the console as text."""
#     try:
#         statement = input("Please type your command: ")
#         print(f"user said: {statement}\n")
#         return statement.lower()
#     except Exception as e:
#         print("An error occurred. Please try again.")
#         return "None"


def search_wikipedia(query):
    """Search Wikipedia for the given query."""
    speak('Searching Wikipedia...')
    results = wikipedia.summary(query, sentences=3)
    speak("According to Wikipedia")
    print(results)
    speak(results)


def open_website(url, site_name):
    """Open a website in a new browser tab."""
    webbrowser.open_new_tab(url)
    speak(f"{site_name} is open now")
    time.sleep(2)


def get_weather():
    """Fetch weather information for a city using OpenWeatherMap API."""
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    speak("What's the city name?")
    city_name = take_command()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data.get("cod") != "404":
        main = weather_data["main"]
        temp = main["temp"]
        humidity = main["humidity"]
        description = weather_data["weather"][0]["description"]
        speak(
            f"The temperature is {temp - 273.15:.2f} degrees Celsius, humidity is {humidity} percent, and the weather is {description}.")
        print(f"Temperature: {temp - 273.15:.2f}°C\nHumidity: {humidity}%\nDescription: {description}")
    else:
        speak("City Not Found")


def get_time_date():
    """ Respond with the current time, date, or both based on user input. param user_input: String input from the user indicating what they want (time, date, or both)."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%B %d, %Y")

    if 'time' in statement and 'date' in statement:
        speak(f"Today is {current_date} and the time is {current_time}.")
        print(f"Today is {current_date} and the time is {current_time}.")

    elif 'time' in statement:
        speak(f"The time is {current_time}.")
        print(f"The time is {current_time}.")

    elif 'date' in statement:
        speak(f"Today's date is {current_date}.")
        print(f"Today's date is {current_date}.")


def handle_computational_question():
    """Answer computational and geographical questions using WolframAlpha."""
    speak('What question would you like to ask?')
    question = take_command()
    app_id = "R2K75H-7XHELAL35X"
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    answer = next(res.results).text
    speak(answer)
    print(answer)


def take_photo():
    """Take a photo using the webcam."""
    ec.capture(0, "robo camera", "img.jpg")


def shutdown_pc():
    """Shutdown the PC after a warning."""
    speak("Your PC will log off in 10 seconds. Please close all applications.")
    subprocess.call(["shutdown", "/l"])


# Main Execution
if __name__ == '__main__':
    speak("Loading your AI GENERAL ASSISTANT - BAY MAX")
    wish_me()

    while True:
        speak("Tell me, how can I help you now?")
        statement = takeCommand()

        if statement in ["good bye", "ok bye", "stop", "exit"]:
            speak('Your personal assistant Bay Max is shutting down, Goodbye!')
            print('Your personal assistant Bay Max is shutting down, Goodbye!')
            break

        # Command Handling
        if 'wikipedia' in statement:
            search_wikipedia(statement.replace("wikipedia", ""))

        elif 'open youtube' in statement:
            open_website("https://www.youtube.com", "YouTube")

        elif 'open google' in statement:
            open_website("https://www.google.com", "Google")

        elif 'open gmail' in statement:
            open_website("https://mail.google.com", "Gmail")

        elif 'open stackoverflow' in statement:
            open_website("https://stackoverflow.com", "Stack Overflow")

        elif 'weather' in statement:
            get_weather()

        elif statement in ["time", "date"]:
            get_time_date()

        elif 'news' in statement:
            open_website("https://timesofindia.indiatimes.com/home/headlines", "Times of India")

        elif 'camera' in statement or 'take a photo' in statement:
            take_photo()

        elif 'search' in statement:
            query = statement.replace("search", "")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            speak("Here are the search results")
            time.sleep(2)

        elif 'ask' in statement:
            handle_computational_question()

        elif 'shutdown' in statement:
            shutdown_pc()

        time.sleep(2)


