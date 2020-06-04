import os 
from gtts import gTTS

print("Converting your text to sound . . .")
tts = gTTS(text='Please collect your cash.', lang='en')
tts.save("4.mp3")
print("Starting audio. . .")
os.system('start 4.mp3')
print("Thank You !!")
