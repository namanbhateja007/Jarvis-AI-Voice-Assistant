import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from google import genai


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


newsapi = "YOUR_NEWS_API_KEY"


def aiProcessor(command):
    client = genai.Client(api_key="YOUR_API_KEY")

    chat = client.chats.create(
        model="gemini-3.6-flash"
    )

    response = chat.send_message(command)

    return response.text

def processcommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")

    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "")
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():

        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:

            data = response.json()

            articles = data.get("articles", [])

            print("Number of articles:", len(articles))

            for article in articles:
                print(article["title"])
                speak(article["title"])

        else:
            print("Failed to fetch news.")

    else:
        output = aiProcessor(c)
        speak(output)


if __name__ == "__main__":

    speak("Initialising Jarvis....")

    while True:

        r = sr.Recognizer()

        print("Recognizing...")

        try:

            with sr.Microphone() as source:

                print("Listening...")

                audio = r.listen(
                    source,
                    timeout=3,
                    phrase_time_limit=2
                )

            word = r.recognize_google(audio)

            print("You said:", word)

            if "jarvis" in word.lower():

                print("WAKE WORD DETECTED")

                speak("Yes Sir, I am listening...")

                with sr.Microphone() as source:

                    print("Jarvis Active...")

                    audio = r.listen(source)

                command = r.recognize_google(audio)

                print("Command:", command)

                processcommand(command)

        except Exception as e:

            print("Error:", e)
