# AI Radio Project
# Restart - 2023

# ------ Pygame Channels ------
# Channel 1 = Music
# Channel 2 = Commentary
# Channel 3 = Indent
# Channel 4 = Adverts

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
musicpath = "\\music"
commentarypath = "\\commentary"
advertpath = "\\advert"
song = "C:\\Users\\Samuel\\Documents\\AI Radio\\airadio\\music\\04 I Wonder.mp3"

# ------ Announcement Locations -----
# 1 = start of song
# 2 = end of song
# 3 = song finished
# 4 = none

# ------ Music Handler ------
def music():
    # Decide song announcements
    if songannounce == True:
        #announcelocation = random.randint(1,4)
        announcelocation = 1
    
    print(f"[INFO] Location for song announcement is: {announcelocation}. Starting song {song}...")

    # Start song
    sound = pygame.mixer.Sound(song)
    channel = sound.play()
    volume = 1
    sound.set_volume(volume)
    audio = EasyID3(song)

    print(f"[SONG] Song {audio['title']} by {audio['artist']} is playing...")

    # If an announcement will occur, generate text to speech now
    if announcelocation != 4:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        text = f"Here's {audio['artist']} with {audio['title']}"
        engine.say(text)
        print(f"[TTS] Generated TTS. Waiting for location...")
        print(f"[TTS] TTS Message: {text}")

    if announcelocation == 1:
        # Wait for song to start
        time.sleep(5)

        print("[TTS] Preparing for TTS... fading down...")
        # Fade down
        for i in range(0,8):
            volume = volume - 0.1
            sound.set_volume(volume)
            time.sleep(0.1)
        
        print(f"[TTS] Playing TTS.")
        # Run TTS
        engine.runAndWait()
        
        time.sleep(1)
        
        print("[TTS] Fading up...")
        # Fade up
        for i in range(0,8):
            volume = volume + 0.1
            sound.set_volume(volume)
            time.sleep(0.1)
        print("[TTS] TTS Complete.")
    while channel.get_busy() == True:
        time.sleep(0.5)
    print("[SONG] Song complete.")

music()