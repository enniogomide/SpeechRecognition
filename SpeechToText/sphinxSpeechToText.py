#
# This program uses the SpeechRecognition library to convert 
# speech to text using the Sphinx recognizer.
#
# The program listens to the microphone and prints the recognized
# speech to the console.
# 
# The voice recognition was not good.
#  
import os

import speech_recognition as sr

# obtain audio from the microphone
text_recognized = ""
while text_recognized != "exit":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    #recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))