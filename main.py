# AI Radio Project
# Restart - 2023

# ------ Imports ------
import pygame
import random
import time
import os
import pyttsx3
from mutagen.easyid3 import EasyID3

pygame.init()
pygame.mixer.init()

# ------ Hardcoded Variables ------
indent = True
songannounce = True
commentary = True
adverts = True
path = os.getcwd()
pathtype = "\\"
musicpath = path + pathtype + "music"
commentarypath = pathtype + "commentary"
advertpath = pathtype + "advert"
music = []

# ------ Generate Arrays ------
musicfiles = os.listdir(musicpath)
print(musicfiles)

# ------ Announcement Locations -----
# 1 = start of song
# 2 = end of song
# 3 = song finished
# 4 = none

# ------ Logging Function ------
def log(type, content):
    # Writes to a log for each function, and a main log too
    string = f"{type.upper()} {content}"
    filename = f"{type.lower()}.log"
    speclog = open(filename, "a")
    mainlog = "main.log", "a"
    speclog.write(string)
    mainlog.write(string)
    speclog.close()
    mainlog.close()
    print(string)

# ------ Music Handler ------
def music():
    # Select song
    song = musicpath + pathtype + random.choice(musicfiles)
    # Decide song announcements
    if songannounce == True:
        announcelocation = random.randint(1,3)
    else:
        announcelocation = "off"
    
    log("song", f"Location for song announcement is: {announcelocation}. Starting song {song}...")

    # Start song
    sound = pygame.mixer.Sound(song)
    channel = sound.play()
    volume = 1
    sound.set_volume(volume)
    audio = EasyID3(song)

    log("song", f"Song {audio['title']} by {audio['artist']} is playing...")

    # If an announcement will occur, generate text to speech now
    if announcelocation != 4:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        text = f"Here's {audio['artist']} with {audio['title']}"
        engine.say(text)
        log("tts", f"Generated TTS. Waiting for location...")
        log("tts", f"TTS Message: {text}")

    if announcelocation == 1:
        # Wait for song to start
        time.sleep(5)

        log("tts", "Preparing for TTS... fading down...")
        # Fade down
        for i in range(0,8):
            volume = volume - 0.1
            sound.set_volume(volume)
            time.sleep(0.1)
        
        log("tts", f"Playing TTS.")
        # Run TTS
        engine.runAndWait()
        
        time.sleep(1)
        
        log("tts", "Fading up...")
        # Fade up
        for i in range(0,8):
            volume = volume + 0.1
            sound.set_volume(volume)
            time.sleep(0.1)
        print("tts", "TTS Complete.")
    # Wait for song to complete...
    while channel.get_busy() == True:
        time.sleep(0.5)
    print("song", "Song complete.")


music()