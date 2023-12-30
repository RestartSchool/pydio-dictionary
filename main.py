# Pydio
# Restart - 2023

# ------ Logging Function ------
def log(type, content):
    # Writes to a log for each function, and a main log too
    printstring = f"[{type.upper()}] {content}"
    filestring = f"\n[{type.upper()}] {content}"
    filename = f"{type.lower()}.log"
    speclog = open(filename, "a")
    mainlog = open("main.log", "a")
    speclog.write(filestring)
    mainlog.write(filestring)
    speclog.close()
    mainlog.close()
    print(printstring)

# Initial Log - Import time, read current system time and log it
import time
t = time.localtime()
log("init", f"{time.strftime('%H:%M:%S', t)} - Welcome to Pydio.")

# ------ Error Handler Function ------
def errorhandler(type, error):
    print("\n[FATAL] The error handler has been called.")
    t = time.localtime()
    log("fatal", f"Pydio has crashed during {type} stage, the time is {time.strftime('%H:%M:%S', t)}. Details of the log are below:")
    log("fatal", error)
    exit(1)

# ------ Imports ------
try:
    import pygame # Pygame - Audio
    import random # Random - Random
    import os # OS - Several File Functions
    import pyttsx3 # PYTTSX3 - Text to Speech
    from mutagen.easyid3 import EasyID3 # Mutagen (EasyID3) - Audio Metadata
    log("init", "Dependencies loaded.")
except ModuleNotFoundError as error:
    log("init", "A module has failed to import! Please ensure you have installed all required dependencies. The error handler will be called.")
    errorhandler("init", error)

# Initialize Pygame
try:
    pygame.init()
    pygame.mixer.init()
    log("init", "Pygame init success!")
except pygame.error as error:
    log("init", "Pygame initialisation has failed! The error handler will be called.")
    errorhandler("init", error)

# ------ Hardcoded Variables ------
indent = True
songannounce = True
commentary = True
adverts = True
path = os.getcwd()
pathtype = "\\"
musicpath = path + pathtype + "music"
commentarypath = path + pathtype + "commentary"
advertpath = path + pathtype + "advert"
music = []

# ------ Generate Arrays ------
# Music Files
log("init", "Detecting music files...")
musicfiles = os.listdir(musicpath)
log("init", f"Music detection complete, {len(musicfiles)} music files detected.")
# Commentary Files
log("init", "Detecting commentary files...")
commentaryfiles = os.listdir(commentarypath)
log("init", f"Commentary detection complete, {len(commentaryfiles)} commentary files detected.")
# Advert Files
log("init", "Detecting advert files...")
advertfiles = os.listdir(advertpath)
log("init", f"Advert detection complete, {len(advertfiles)} advert files detected.")


log("init", "Init complete! Handing over to main function.")
# ------ Announcement Locations -----
# 1 = start of song
# 2 = end of song
# 3 = song finished
# "off" = none

# ------ Music Handler ------
def music():
    # Select song
    song = musicpath + pathtype + random.choice(musicfiles)
    # Decide song announcements
    if songannounce == True:
        announcelocation = random.randint(1,1)
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
        log("tts", "TTS Complete.")
    # Wait for song to complete...
    # while channel.get_busy() == True:
    #     time.sleep(0.5)
    time.sleep(5)
    sound.stop()
    log("song", "Song complete.")

def play(type):
    if type == "commentary":
        log("comm", "Commentary selected.")
        # Pick random commentary and play it
        selection = commentarypath + pathtype + random.choice(commentaryfiles)
        sound = pygame.mixer.Sound(selection)
        channel = sound.play()
        log("comm", f"Playing {selection}.")
        while channel.get_busy() == True:
            time.sleep(0.5)
        log("comm", "Complete.")
    elif type == "advert":
        advertsplayed = []
        # Decide amount of ads
        log("ad", f"Advert selected.")
        if len(advertfiles) >= 4:
            rngadvertamount = random.randint(2,4)
        else:
            rngadvertamount = len(advertfiles)
        log("ad", f"RNG has decided {rngadvertamount} ads will be played!")
        for i in range(0, rngadvertamount):
            # Check if ad has already been played
            while True:
                selection = advertpath + pathtype + random.choice(advertfiles)
                log("ad", f"Trying {selection}...")
                if advertsplayed.count(selection) == 0:
                    advertsplayed.append(selection)
                    log("ad", f"{selection} has not been played yet! Selecting it.")
                    break
                else:
                    log("ad", f"{selection} has already been played, trying again...")
                    continue
            # Play ad
            log("ad", f"Playing {selection}.")
            sound = pygame.mixer.Sound(selection)
            channel = sound.play()
            while channel.get_busy() == True:
                time.sleep(0.5)
        log("ad", "Complete.")

def main():
    while True:
        if len(musicfiles) >= 4:
            rngtriggeradvert = random.randint(2,4)
        else:
            rngtriggeradvert = len(musicfiles)
        log("main", f"RNG has decided {rngadvertamount} songs will be played before adverts!")
        for i in range(0, rngtriggeradvert):
            rngcommentary = random.randint(0,1)
            log("main", "Commentary selected.")
            if rngcommentary == 0:
                log("main", "No commentary selected!")
                log("main", "Calling music function.")
                music()
            elif rngcommentary == 1:
                log("main", "Commentary selected!")
                log("main", "Calling commentary function.")
                play("commentary")
                log("main", "Calling music function.")
                music()
        if adverts == True:
            play("advert")
        else:
            continue

main()