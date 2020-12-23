"""
Import python packages
"""

#import subprocess
from strings import Strings
import datetime
# for timezone()
import pytz

import subprocess
from datetime import datetime
import os

import filePath
from Memory import Memory

#import playsound
import speech_recognition as sr
from gtts import gTTS

import numpy as np
import re
import pandas as pd
import pickle
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

personName='' #to store name of the user

"""
read model, word2vec and data file
"""
filename = './models/nlu_2.0.sav'
nlu = pickle.load(open(filename, 'rb'))
filename = './models/word2vec_2.0.sav'
word2vec = pickle.load(open(filename, 'rb'))
filename = './data/data_2.0.csv'
df = pd.read_csv(filename)

"""
create object of memory class
"""
m = Memory()

"""
main method for chatbot
"""

def chat(ip,correctNameGiven):
    """
    To check whether user has given his name or not
    """
    if correctNameGiven==False:
        name=recognizeName(ip.lower())
        if (name == -1):
            return (-1)
        else:
            return(Strings.hello + name.title())

    test = []
    review = re.sub('[^a-zA-Z]', ' ', ip)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review]
    review = ' '.join(review)
    test.append(review)

    x = word2vec.transform(test).toarray()

    ans = nlu.predict(x)

    m.push(ans[0])

    count = 0

    for i in range(0, 9):
        if m.store[9] == m.store[i]:
            count += 1
    output = ''
    if count >= len(df[df['id'] == ans[0]]['answer'].values):
        output = df[df['id'] == ans[0]]['answer'].values[len(df[df['id'] == ans[0]]['answer'].values) - 1]
    else:
        output = df[df['id'] == ans[0]]['answer'].values[count]

    output = clean(output)

    if 'task' in ans[0]:
        temp = doTask(output, test[0])
        if type(temp) == str:
            output = temp

    #speek(output)
    return output

"""
method for cleaning output text
"""
def clean(output):
    global personName
    if("{" in output):
        output = output.replace("{name}", personName)
    return output

"""
method for speek
"""
def speek(text):
    tts = gTTS(text= text, lang = "en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

"""
get input from mic
"""
def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('0')
        audio = r.listen(source, timeout=2, phrase_time_limit=5)
        print('1')
        said = ""
        try:
            print('2')
            said = r.recognize_google(audio)
            print('3')
            return said
        except Exception as e:
            return str(e)

"""
for automation in computer
"""
def doTask(output, test):
    """try except block: if file not found then program don't get crashed"""
    print(test)
    task = ""
    try:
        if 'firefox' in test:
            path = filePath.root_path + filePath.firefox
            os.system(path)
            task = "firefox"

        elif 'terminal' in test:
            os.system(filePath.terminal)
            task = "terminal"

        elif 'webcam' in test:
            path = filePath.root_path + filePath.webcam
            os.system(path)
            task = "webcam"

        # elif 'calculator' in output:
        #     subprocess.call(filePath.calculator)
        #    os.system(path)

        # elif 'file manager' in output:
        #     subprocess.call(filePath.files)
        #    os.system(path)

        elif 'vs code' in test:
            path = filePath.root_path + filePath.vsCode
            os.system(path)
            task = "vs code"

        elif 'pycharm' in test:
            path = filePath.root_path + filePath.pycharm
            os.system(path)
            task = "pycharm"

        elif 'anaconda navigator' in test:
            path = filePath.root_path + filePath.conda
            os.system(path)
            task = "anaconda navigator"

        # elif 'text editor' in output:
        #     subprocess.call(filePath.text)
        #    os.system(path)

        elif 'discord' in test:
            path = filePath.root_path + filePath.discord
            os.system(path)
            task = "discord"
            #subprocess.call(filePath.discord)
        elif 'thunderbird' in test:
            path = filePath.root_path + filePath.email
            os.system(path)
            task = "thunderbird"

        elif 'time' in output:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return current_time

        else:
            return "not available"

    except Exception as e:
        return str(e)

"""
Greet according to time
"""
def greetAtStart():
    # using now() to get current time
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    current_time.hour
    if current_time.hour < 12:
        return(Strings.gm)
    elif current_time.hour == 12:
        return(Strings.gNoon)
    elif current_time.hour > 12 and current_time.hour < 18:
        return(Strings.gAfter)
    elif current_time.hour >= 18:
        return(Strings.ge)

"""
getting name of person from the user input
"""
def recognizeName(user_ip):
    global personName
    ip_list=user_ip.split()
    for i in ip_list:
        data=np.load('./data/names/'+i[0]+'.npy',allow_pickle=True)
        for j in data:
          if i==j:
            personName=i
            return(i)
    return(-1)

