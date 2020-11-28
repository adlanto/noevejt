# **************************************** NOEVE Jungle Tracker v0.1 alpha ****************************************

import gtts
import time
from pygame import mixer
import os

class AUDIOS:
    POSITIONS = {}


def welcome():
    mixer.init()
    if not os.path.exists("audios/welcome.mp3"):
        tts = gtts.gTTS("Welcome to the no eve jungle tracker. Press tab inside game to init", lang="en")
        tts.save("audios/welcome.mp3")
    mixer.music.load("audios/welcome.mp3")
    mixer.music.play()
    time.sleep(5.5)


def init_success(jungler_name):
    # Create a mp3 file with text to speech and play it
    try:
        tts = gtts.gTTS("Init successful, tracked jungle is" + jungler_name, lang="en")
        tts.save("audios/jungler_name.mp3")
        time.sleep(0.1)
        mixer.music.load("audios/jungler_name.mp3")
        mixer.music.play()
        time.sleep(5.0)
    except:
        print("Error: Failed to play Audio \"jungler_name.mp3\"")


def position(position):
    if not os.path.exists("audios/" + position + ".mp3"):
        tts = gtts.gTTS(position, lang="en")
        tts.save("audios/"+position+".mp3")
    mixer.music.load("audios/"+position+".mp3")
    mixer.music.play()
    time.sleep(1.0)


def no_smite():
    if not os.path.exists("audios/no_smite.mp3"):
        tts = gtts.gTTS("There is no smite in enemy team", lang="en")
        tts.save("audios/no_smite.mp3")
    mixer.music.load("audios/no_smite.mp3")
    mixer.music.play()
    time.sleep(3)


def quit():
    if not os.path.exists("audios/quit.mp3"):
        tts = gtts.gTTS("Thank you for using no eve jungle tracker", lang="en")
        tts.save("audios/quit.mp3")
    mixer.music.load("audios/quit.mp3")
    mixer.music.play()
    time.sleep(4.0)
