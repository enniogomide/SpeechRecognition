
from gtts import gTTS
from IPython.display import Audio

with open("./Input_text/texto.txt", "r") as arquivo:
	texto_leitura = arquivo.read()

language = "pt"


gtts_object = gTTS(text = texto_leitura, 
                  lang = language,
                  tld='com.br',
                  slow = False)

gtts_object.save("./Voice_Generated/gtts_01.mp3")


Audio("./Resultado/gtts_01.mp3", autoplay=True)
