import pyttsx3
import speech_recognition as sr
import datetime
import os
import sys
import cv2
import requests
import pywhatkit
import webbrowser
import wikipedia
import pyjokes
import operator
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer, QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from paradoxNewUi import Ui_MainWindow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#this function converts the text to speech.
def talk(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

#this function is to wish the user based on the time.
def wish():
    time = int(datetime.datetime.now().hour)
    
    if time>=6 and time<12:
        talk('Good morning boss')
    elif time>=12 and time<15:
        talk('Good afternoon boss')
    else:
        talk('Good evening boss')
    talk('How can I help you?')

#this is the function to retrieve the news
def news():
    news_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=637e2a5217e4400999a749d3c304b074'
    main_page = requests.get(news_url).json()
    articles = main_page["articles"]
    head = []
    day=["first","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        talk(f'todays {day[i]} news is:{head[i]}')


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.taskExecution()
         


    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening...')
            r.pause_threshold = 2
            audio = r.listen(source,timeout=5,phrase_time_limit=5)

        try:
            print('recognizing....')
            query = r.recognize_google(audio,language= 'en-in')
            print(f"user said:{query}")

        except Exception as e:
                talk("say that again please..")
                return "none"
        return query


    def taskExecution(self):
        wish()
        while True:

            self.command = self.takeCommand().lower()

            #some user commands tasks code.
            
            if 'open notepad' in self.command:
                talk('opening notepad ++')
                os.startfile("C:\\Program Files\\Notepad++\\notepad++.exe")
            elif 'close notepad' in self.command:
                talk('okay boss, closing notepad++')
                os.system("taskkill /f /im notepad++.exe")
            elif 'command prompt' in self.command:
                talk('opening command prompt')
                os.system("start cmd")
            elif 'open word' in self.command:
                talk('opening Mircrosoft word')
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
            elif 'close word' in self.command:
                talk('closing word')
                os.system("taskkill /f /im WINWORD.EXE")
            elif 'open powerpoint' in self.command:
                talk('opening microsoft powerpoint')
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
            elif 'close powerpoint' in self.command:
                talk('closing powerpoint')
                os.system("taskkill /f /im POWERPNT.EXE")
            elif 'open excel' in self.command:
                talk('opening microsoft excel')
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
            elif 'close excel' in self.command:
                talk('closing excel')
                os.system("taskkill /f /im EXCEL.EXE")
            elif 'open brave' in self.command:
                talk('opening brave')
                os.startfile("C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe")
            elif 'close brave' in self.command:
                talk('closing brave')
                os.system("taskkill /f /im brave.exe")
            elif 'open edge' in self.command:
                talk('opening edge')
                os.startfile("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            elif 'close edge' in self.command:
                talk('closing edge')
                os.system("taskkill /f /im msedge.exe")
            elif 'hi' in self.command or 'hey' in self.command:
                talk('hello boss.')
            elif 'open camera' in self.command:
                talk('opening camera')
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break;
                cap.release()
                cv2.destroyAllWindows()
            elif 'news' in self.command or 'headlines' in self.command:
                talk('ok boss, give me some time to fetch the current headlines of the day')
                news()
            elif 'play' in self.command:
                song = self.command.replace('play', '')
                talk(f"playing {song}")
                pywhatkit.playonyt(song)
            elif 'get some music' in self.command :
                talk('what song should I play for you boss?')
                music = self.takeCommand().lower()
                pywhatkit.playonyt(music)
            elif 'time' in self.command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('the time is '+time)
            elif 'search' in self.command or 'meaning' in self.command:
                value = self.command.replace('search', '')
                info = wikipedia.summary(value,1)
                talk('according to wikipedia')
                talk(info)
            elif 'open youtube' in self.command:
                talk('opening youtube')
                webbrowser.open('www.youtube.com')
            elif 'open facebook' in self.command:
                talk('opening facebook')
                webbrowser.open('www.facebook.com')
            elif 'open linkedin' in self.command:
                talk('opening linkedin')
                webbrowser.open('www.linkedin.com')
            elif 'open google' in self.command:
                talk('Boss, what should I search in google?')
                search = self.takeCommand().lower()
                webbrowser.open(f'{search}')
            elif 'tell me a joke' in self.command:
                talk(pyjokes.get_joke())
            elif 'shutdown the system' in self.command:
                talk('shuting down the system boss')
                os.system('shutdown /s /t 5')
            elif 'restart the system' in self.command:
                talk('restarting the system boss')
                os.system("shutdown /r /t 5")
            elif 'hello' in self.command:
                talk('hello sir! may I help you for something?')
            elif 'how are you' in self.command:
                talk('I am fine sir. How about you?')
            elif 'fine' in self.command or 'good' in self.command:
                talk('its good to hear from you sir')
            elif 'paradox' in self.command:
                talk('yes boss, I am here.')
            elif 'thank you' in self.command:
                talk('your welcome boss')
            

            #mathematical calculations
            elif 'do some calculations' in self.command or 'calculate' in self.command:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    talk('say something to calculate, for example 12 plus 12')
                    print('listening...')
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_stringer = r.recognize_google(audio)
                print(my_stringer)
                def get_operator_fn(op):
                    return {
                            '+' : operator.add,
                            '-' : operator.sub,
                            'x' : operator.mul,
                            'divided' : operator.__truediv__,
                        }[op]
                def eval_binary_expr(op1,oper,op2):
                    op1,op2 = int(op1),int(op2)
                    return get_operator_fn(oper)(op1,op2)
                talk('your result is ')
                talk(eval_binary_expr(*(my_stringer.split())))

            elif 'where i am' in self.command or 'where am i' in self.command:
                talk('wait boss, let me check')
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    talk(f'sir i think we are in {city} of {country}')
                except Exception as e:
                    talk('sorry boss, due to some network issues i did not get the location.')
                    pass


            elif 'sleep' in self.command or 'no thanks' in self.command:
                talk('thank you boss. Have a good day')
                sys.exit()

            

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/main.gif")
        self.ui.main.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/circle.gif")
        self.ui.inner_crc.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/initial.gif")
        self.ui.initial.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/void.gif")
        self.ui.outer_crc.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/reload.gif")
        self.ui.load.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/NAGENDRA/OneDrive/Desktop/paradoxuitools/alien.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    
    def showTime(self):
        current_time = QTime.currentTime()
        now = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        self.ui.textBrowser.setText(label_time)
        


app = QApplication(sys.argv)
paradox = Main()
paradox.show()
exit(app.exec_())



        
        