import speech_recognition as sr
import webbrowser
import datetime
import calendar
import wikipedia
import pyttsx3
import requests
from twilio.rest import Client
import smtplib
import pywhatkit



def speechTotext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')

        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 100
        # recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,0,4)
        try:
            print('recognizing...')
            data = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return 'not understanding'
        print('you said',data)
        return data


def textTospeech(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate',130)
    engine.say(x)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        textTospeech("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        textTospeech("Good Afternoon Sir !")

    else:
        textTospeech("Good Evening Sir !")

    assname = ("Jarvis")
    textTospeech("I am your Assistant")
    textTospeech(assname)
    textTospeech('how can i help you')

def weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key=?&q={city}'
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)
        posts = response.json()
        print(posts['current']['temp_c'])
        print(posts['current']['condition']['text'])
        print(posts['location']['name'])
        print(posts)
        return {'temp':posts['current']['temp_c'],'env':posts['current']['condition']['text'],'location':posts['location']['name']}
    except:
        return {}

def Message(msg):
    account_sid = 'account_sid'
    auth_token = "auth_token"
    client = Client(account_sid, auth_token)

    call = client.messages.create(
        body=f"{msg}",
        to="mobile no.",
        from_="mobile no.",
    )

def call():
    account_sid = ''
    auth_token = ""
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to="",
        from_="",
    )

def sendEmail(content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Enable low security in gmail
    server.login('user', '')
    server.sendmail('from', 'to',f'{content}')
    server.close()

def News():
    data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=?')
    news = data.json()
    for i in enumerate(news['articles']):
        index = i[0] +1
        textTospeech(f'number {index}  .' + i[1]['title'])


if __name__ == "__main__":
    counter =0
    wishMe()
    while True:
        query = speechTotext().lower()
        if 'time right now' in query or 'time' in query or 'time now' in query:
            today = datetime.datetime.now()
            h = today.hour
            m = today.minute
            textTospeech(f'{h} {m} ')

        elif 'how are you' in query or 'how r u' in query:
            textTospeech("I am fine, Thank you")
            textTospeech("How are you, Sir")

        elif 'fine' in query or "good" in query:
            textTospeech("It's good to know that your fine")

        elif 'marry to me' in query:
            textTospeech('sorry , but I am not interested')

        elif 'your education' in query or 'your qualification' in query:
            textTospeech('i am not interested in school or colleges , but i am still learning outside of the world')

        elif 'your age' in query:
            textTospeech('i am not sure about my age, but i have been made by avinash')

        elif "what's your name" in query or "What is your name" in query:
            textTospeech("My friends call me")
            textTospeech('jarvis 1 point o')

        elif "who made you" in query or "who created you" in query:
            textTospeech("I have been created by Avinash.")

        elif "who are you" in query:
            textTospeech("I am your virtual assistant created by Avinash")

        elif 'date today' in query or 'today date' in query or 'date' in query or 'today' in query:
            today = datetime.datetime.today()
            day = today.day
            month = today.month
            year = today.year
            mn = calendar.month_name[month]
            textTospeech(f'today date is {day} .  {mn}  . {year}')

        elif 'weather' in query or 'temperature' in query:
            splitdata = query.split(' ')
            city = []
            for q in splitdata:
                try:
                    if q not in ['what','how','is','the','temperature','weather','of','ok','tell','me']:
                        city.append(q)
                except:
                    textTospeech('please specify city name')

            data = weather(city[0])
            if len(data) !=0:
                location = data['location']
                temp = data['temp']
                env = data['env']
                textTospeech(f'{location} temperature is {temp} celsius {env}')
            else:
                textTospeech('sorry for this , please spell it correct')

        elif 'text message' in query or 'write a message' in query:
            textTospeech('what is your text . you want to send')
            text = speechTotext()
            Message(text)
            textTospeech('message sent successfully')
            textTospeech('now what else i can do for you')

        elif 'make a call' in query or 'you call me' in query:
            textTospeech('of course')
            textTospeech('we are calling ...')
            call()
            break

        elif 'send a email' in query or 'send email' in query:
            textTospeech('what message you want to send')
            text = speechTotext()
            sendEmail(text)
            textTospeech('message sent successfully')
            textTospeech('now what else i can do for you')

        elif 'wikipedia' in query or 'what do you know' in query:
            textTospeech('according to wikipedia ')
            splitdata = query.split(' ')
            lst =[]
            for q in splitdata:
                try:
                    if q not in ['wikipedia','what','is','do','you','say','know','about']:
                        lst.append(q)
                except:
                    textTospeech('sorry , i am not able to find this information on wikipedia')
            string = ' '.join(lst)
            if len(lst) ==1:
                string = 'about '+string
            try:
                text = wikipedia.summary(f'{string}', sentences=1)
            except:
                textTospeech('sorry , i am not able to find this information on wikipedia')
            else:
                textTospeech(text)

        elif 'news' in query or 'top headlines' in query:
            News()
            textTospeech('this is top headlines')

        elif 'search' in query or 'google' in query:
            splitdata = query.split(' ')
            lst =[]
            for q in splitdata:
                try:
                    if q not in ['search','google','on']:
                        lst.append(q)
                except:
                    textTospeech('something went wrong')
            string = ' '.join(lst)
            pywhatkit.search(string)
            break

        elif 'open google' in query or 'google open' in query:
            textTospeech('wait google is being open')
            webbrowser.open('www.google.com')
            break

        elif 'thankyou jarvis' in query or 'ok thank you' in query or 'thankyou' in query or 'ok thank u' in query or 'stop' in query:
            textTospeech('ok, bye you can call me again')
            break
        else:
            if counter==3:
                exit()
            counter+=1
            textTospeech('if you are getting your wish results then specify that a bit more')
            textTospeech('like open wikipedia or open google')


