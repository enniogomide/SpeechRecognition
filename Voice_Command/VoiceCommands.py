#import section

import os
import io
from datetime import datetime
import time

import speech_recognition as sr
from gtts import gTTS

import pygame

import pyjokes
import wikipedia
import webbrowser
import winshell
from pygame import mixer
from googletrans import Translator

#
# function to translate text used inside the routine
#
def translate_text(text, language='pt'):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=language)
    try:
        translated_joke = translated_text.text
    except AttributeError:
        translated_joke = ""
    except:
        translated_joke = ""
    
    return translated_joke

#
# standard message to play when the speech is not recognized
#
def standard_message():
    text_to_speech("Não entendi o que você disse. Vamos tentar novamente.")
    print("Nao entendi o que voce disse. Vamos tentar novamente.")
#
# convert text to speech
#
def text_to_speech(text_to_convert, language='pt'):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    # if the audio is not playing, play the audio
    if not mixer.music.get_busy():
        # object gTTS wiht the text and language
        tts = gTTS(text=text_to_convert, lang=language)
        
        # audio is saved in memory buffer(not in file)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)  # return to the beginning of the buffer
        
        # Inicialize the pygame to reproduce the audio
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        # Wait the audio playing finish 
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

#get mic audio
def get_audio(language='pt'):
    language_spoken = language
    r = sr.Recognizer()
    get_the_audio = ""
    while get_the_audio != "sair":
        with sr.Microphone() as source:
            r.pause_threshold = 1
            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            said = ""
            try:
                said = r.recognize_google(audio, language=language_spoken)
                print(said)
                get_the_audio = "sair"
            except sr.UnknownValueError:
                standard_message()
            except sr.RequestError:
                text_to_speech("Sinto muito. O serviço não esta disponível")
                print("Sinto muito. O serviço não esta disponível")
                get_the_audio = "sair"
            except LookupError:                            # speech is unintelligible
                message_to_exibit()
            except:    
                message_to_exibit() 
    return said.lower()

#play music
def playmusic(directory, song):
    mixer.init()
    mixer.music.load(directory + song)
    mixer.music.play()

#stop music
def stopmusic():
    mixer.music.stop()

#function to respond to commands
def respond(text, count_song, playing_music):
    print("Texto do áudio: " + text)
    if 'youtube' in text:
        text_to_speech("O que deseja pesquisar?")
        keyword = get_audio()
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            text_to_speech(f"Aqui o que encontramos com a palavra {keyword} no youtube")
    elif 'facebook' in text:
        url = f"https://facebook.com"
        webbrowser.get().open(url)
        text_to_speech(f"Abri o facebook para voce")
    elif 'instagram' in text:
        url = f"https://www.instagram.com"
        webbrowser.get().open(url)
        text_to_speech(f"O instagram foi aberto. Faça tuas pesquisas")
    elif 'pesquisar' in text:
        text_to_speech("Que assunto deseja pesquisar?")
        query = get_audio()
        if query !='':
            wikipedia.set_lang("pt")
            result = wikipedia.summary(query, sentences=3)
            text_to_speech("De acordo com a wikipedia, temos...")
            print(result)
            text_to_speech(result, language='pt')
    elif 'piada' in text:
        piada_en = pyjokes.get_joke()
        translated_joke = translate_text(piada_en, language='pt')
        try:
            text_to_speech(translated_joke)
        except AttributeError:
            text_to_speech("Desculpe. Não consegui encontrar uma piada em português. Mas tenho em inglês!")
            text_to_speech(piada_en, language='en')
        except:
            text_to_speech("Desculpe. Não consegui encontrar uma piada em português. Mas tenho em inglês!")
            text_to_speech(piada_en, language='en')
    elif 'limpar lixeira' in text:
        recycle_bin_status = list(winshell.recycle_bin())
        if recycle_bin_status != []:
            winshell.ShellRecycleBin().empty(confirm=False, show_progress=False, sound=True)
        text_to_speech("A lixeira está vazia")
    elif 'que horas são' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        text_to_speech(strTime)
    elif 'música' in text or 'playlist' in text:
        text_to_speech("Tocando...")
        
        music_dir = "./Musicas/"
        songs = os.listdir(music_dir)

        if not mixer.music.get_busy():
            if count_song >= (len(songs) - 1):
                count_song = 0
            song_name = songs[count_song].split(".")[0]
            text_to_speech(f"Tocando a música {song_name}")
            print(song_name)
            playmusic(music_dir, songs[count_song])
            count_song += 1
            playing_music = True
    elif 'parar' in text:
        text_to_speech("Parando de tocar.")
        stopmusic()
        playing_music = False
        count_song = 0
    #
    # if the music is not playing, play the next song
    #
    elif not mixer.music.get_busy() and playing_music:
        if count_song >= (len(songs) - 1):
            count_song = 0
        song_name = songs[count_song].split(".")[0]
        text_to_speech(f"Tocando a música {song_name}")
        print(song_name)
        playmusic(music_dir, songs[count_song])
        count_song += 1
        playing_music = True

    return count_song, playing_music

#main function
def main(count_song, playing_music):
    encerrar = False
    text = ""
    while encerrar == False:
        if text == "":
            text_to_speech("As opções disponíveis são: youtube, facebook, instagram, pesquisar, piada, limpar lixeira, que horas são, música ou playlist")
            print("As opções disponíveis são: youtube, facebook, instagram, pesquisar, piada, limpar lixeira, que horas são, música ou playlist")
            text_to_speech("Para parar, basta falar 'finalizar'")
            print("Para parar, basta falar 'finalizar'")
            print("Para parar a música, se estiver tocando, falar 'parar música'")  
        if text not in ("música", "playlist"):
            text_to_speech("Diga o que deseja. Estou ouvindo...")
            print("Diga o que deseja. Estou ouvindo...")
        text = get_audio()
        if text == 'finalizar':
            print("Ok. até a próxima")
            text_to_speech("Ok. até a próxima")
            encerrar = True
        else:
            count_song, playing_music = respond(text, count_song, playing_music)

if __name__ == "__main__":
    playing_music = False
    count_song = 0
    main(count_song, playing_music)
