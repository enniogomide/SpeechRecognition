import speech_recognition as sr

def message_to_exibit():
    print("Não entendi o que você disse. Vamos tentar novamente.")
    print(" ") 


r = sr.Recognizer()
text_recognized = ""
while text_recognized != "sair":

    with sr.Microphone() as source:
        print("Diga alguma coisa! ou <sair> para encerrar")                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

    try:
        text_recognized = r.recognize_google(audio, language="pt")
        print("Você disse: {}" .format(text_recognized))    # recognize speech using Google Speech Recognition
        print(" ")
    except LookupError:                            # speech is unintelligible
        message_to_exibit()
    except:    
        message_to_exibit() 