# Pydio
# Made with ❤️ by Restart
# 2023-2024

try:
    options_dict = {}
    paths_dict = {}

    # ------ Get Path ------
    import os
    path = os.getcwd()
    pathtype = "\\"

    # ------ Logging Function ------
    def log(type, content):
        # Generate log path
        logpath = path + pathtype + "logs"
        # Create log strings
        printstring = f"[{type.upper()}] {content}"
        filestring = f"\n[{type.upper()}] {content}"
        # Create file name
        filename = f"{path}{pathtype}logs{pathtype}{type.lower()}.log"
        # Open Log Files
        speclog = open(filename, "a")
        mainlog = open(f"{path}{pathtype}logs{pathtype}main.log", "a")
        # Write to log files
        speclog.write(filestring)
        mainlog.write(filestring)
        # Close logs and print to terminal
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

    # ------ Interactive Setup - To Boolean Function ------
    def tobool(user):
        if (user == True) or (user.lower() == "y") or (user.lower() == "true"):
            return True
        else:
            return False

    # ------ Interactive Setup - Option Y/N Function ------
    def optionyn(question, default):
        user = str(input(f"{question} ({default}) (y/n)>")).lower()
        if user == "y":
            return tobool(user)
        elif user == "n":
            return tobool(user)
        else:
            print("Invalid option, using default option.")
            return default

    # ------ Interactive Setup - Option Path Function ------
    def optionpath(question, default):
        user = str(input(f"{question} >"))
        if os.path.isdir(user):
            user = user.replace("\\", "\\\\")
            print(user)
            return user
        else:
            print("Path selected is invalid, using default path.")
            default = default.replace("\\", "\\\\")
            print(default)
            return default

    # ------ Interactive Setup ------
    def InteractiveSetup():
        global options_dict, paths_dict

        #Ask questions, add answers to relevant dict
        options_dict["indent"] = optionyn("\nEnable indents? (not implemented yet)", True)
        options_dict["songannounce"] = optionyn("\nEnable TTS song announcements?", True)
        options_dict["commentary"] = optionyn("\nEnable commentary?", True)
        options_dict["adverts"] = optionyn("\nEnable adverts?", True)
        options_dict["testmode"] = optionyn("\nEnable test mode?", True)
        paths_dict['musicpath'] = optionpath("\nPlease enter the music path.", (path + pathtype + "music"))
        paths_dict['commentarypath'] = optionpath("\nPlease enter the commentary path.", (path + pathtype + "commentary"))
        paths_dict['advertpath'] = optionpath("\nPlease enter the advert path.", (path + pathtype + "advert"))

    # ------ Config File Reader ------
    def readconfigfile(path):
        global options_dict, paths_dict

        import configparser
        config = configparser.RawConfigParser()

        # Read options section of config file, add it to dict
        try:
            config.read(path)
            options_dict = dict(config.items('OPTIONS'))
        except configparser.MissingSectionHeaderError as error:
            log("init", "Config file malformed: OPTIONS section missing! Calling error handler...")
            errorhandler("init", error)

        # Read path section of config file, add it to dict
        try:
            config.read(path)
            paths_dict = dict(config.items('PATHS'))
        except configparser.MissingSectionHeaderError as error:
            log("init", "Config file malformed: PATHS section missing! Calling error handler...")
            errorhandler("init", error)


    # ------ Setup Handoff ------
    option = int(input("Please select an option:\n1: Use Interactive Setup\n2. Use Config File (not implemented yet)\n> "))
    while True:
        if option == 1:
            InteractiveSetup()
            break
        elif option == 2:
            readconfigfile("config.cfg")
            break
        else:
            print("Invalid option!")

    # ------ Imports ------
    try:
        import pygame # Pygame - Audio
        import random # Random - Random
        if tobool(options_dict["songannounce"]) == True:
            import pyttsx3 # PYTTSX3 - Text to Speech
            from mutagen.easyid3 import EasyID3 # Mutagen (EasyID3) - Audio Metadata
        else:
            pass
        log("init", "Dependencies loaded.")
    except ModuleNotFoundError as error:
        log("init", "A module has failed to import! Please ensure you have installed all required dependencies. Calling error handler...")
        errorhandler("init", error)

    # ------ Initialize Pygame ------
    try:
        pygame.init()
        pygame.mixer.init()
        log("init", "Pygame init success!")
    except pygame.error as error:
        log("init", "Pygame initialisation has failed! Calling error handler...")
        errorhandler("init", error)

    # ------ Generate Arrays ------
    # Music Files
    log("init", "Detecting music files...")
    musicfiles = os.listdir(paths_dict['musicpath'])
    log("init", f"Music detection complete, {len(musicfiles)} music files detected.")
    # Commentary Files
    if tobool(options_dict["commentary"]) == True:
        log("init", "Detecting commentary files...")
        commentaryfiles = os.listdir(paths_dict['commentarypath'])
        log("init", f"Commentary detection complete, {len(commentaryfiles)} commentary files detected.")
    # Advert Files
    if tobool(options_dict["adverts"]) == True:
        log("init", "Detecting advert files...")
        advertfiles = os.listdir(paths_dict['advertpath'])
        log("init", f"Advert detection complete, {len(advertfiles)} advert files detected.")

    log("init", "Init complete! Handing over to main function.\n")

    # Overview Logs
    log("main", f"Welcome! Overview:\nIndents Activated? {options_dict['indent']}\nSong Announce TTS Activated? {options_dict['songannounce']}\nCommentary Activated? {options_dict['commentary']}\nAdverts Activated? {options_dict['adverts']}\n")
    log("main", f"Path Information:\nRunning Path: {path}\nPath Slash Type: {pathtype}\nMusic Path: {paths_dict['musicpath']}\nMusic Path: {paths_dict['commentarypath']}\nMusic Path: {paths_dict['advertpath']}\n")

    # ------ Announcement Locations -----
    # 1 = before song
    # 2 = start of song
    # 3 = end of song
    # 4 = after song
    # 5 = none

    def tts(metadata, position):
        global engine

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        if len(metadata['artist']) > 1:
            artist = ""
            for i in range(0, len(metadata['artist'])):
                artist = artist + ((metadata['artist'])[i])
                if i != (len(metadata['artist']) - 1):
                    artist = artist + " and "
                else:
                    continue
        else:
            artist = metadata['artist']
        songannouncebefore = [f"Here's {artist} with {metadata['title']}", f"Now, {metadata['title']} by {artist}", f"Now, {artist} with {metadata['title']}", f"Here's {metadata['title']} by {artist}"]
        songannounceafter = [f"That was {artist} with {metadata['title']}", f"You just heard {metadata['title']} by {artist}", f"That was the voice of {artist} with {metadata['title']}", f"You just heard {metadata['title']} by {artist}"]
        if position == "before":
            text = random.choice(songannouncebefore)
            engine.say(text)
        else:
            text = random.choice(songannounceafter)
            engine.say(text)

    # ------ Music Function ------
    def music():
        # Select song, ignoring album art
        while True:
            song = paths_dict['musicpath'] + pathtype + random.choice(musicfiles)
            if ("AlbumArt_" in song) == True or (".png" in song) == True or (".jpg" in song) == True or (".jpeg" in song) == True:
                continue
            else:
                break
        # Decide song announcements
        if tobool(options_dict["songannounce"]) == True:
            announcelocation = random.randint(2,2)
        else:
            announcelocation = 5
        
        # Log
        log("song", f"Location for song announcement is: {announcelocation}. Starting song {song}...")

        # Start song
        if announcelocation == 1:
            pass
        else:
            sound = pygame.mixer.Sound(song)
            channel = sound.play()
            volume = 1
            sound.set_volume(volume)
            if tobool(options_dict["songannounce"])  == True:
                audio = EasyID3(song)
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")
            # If an announcement will occur, generate text to speech now

            if announcelocation == 2:
                tts(audio, "before")
                log("tts", f"Generated TTS. Waiting for location...")
                #log("tts", f"TTS Message: {text}")
                
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
            if tobool(options_dict["testmode"]) == False:
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()
            log("song", "Song complete.")

    # ------ General Playback Function ------
    def play(type):
        if type == "commentary":
            log("comm", "Commentary selected.")
            # Pick random commentary and play it
            selection = paths_dict['commentarypath'] + pathtype + random.choice(commentaryfiles)
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
                    selection = paths_dict['advertpath'] + pathtype + random.choice(advertfiles)
                    log("ad", f"Trying {selection}...")
                    if advertsplayed.count(selection) == 0:
                        # This advert has not been played yet, play it and add it to the played list
                        advertsplayed.append(selection)
                        log("ad", f"{selection} has not been played yet! Selecting it.")
                        break
                    else:
                        # Advert has already been played, continue search
                        log("ad", f"{selection} has already been played, trying again...")
                        continue
                # Play ad
                log("ad", f"Playing {selection}.")
                sound = pygame.mixer.Sound(selection)
                channel = sound.play()
                if tobool(options_dict["testmode"]) == False:
                    while channel.get_busy() == True:
                        time.sleep(0.5)
                else:
                    time.sleep(10)
                    sound.stop()
            log("ad", "Complete.")

    # ------ Main Function ------
    def main():
        while True:
            if len(musicfiles) >= 4:
                rngtriggeradvert = random.randint(2,4)
            else:
                rngtriggeradvert = len(musicfiles)
            if tobool(options_dict["adverts"]) == True:
                log("main", f"RNG has decided {rngtriggeradvert} songs will be played before adverts!")
            else:
                log("main", f"Adverts are disabled.")
            for i in range(0, rngtriggeradvert):
                if tobool(options_dict["commentary"]) == True:
                    rngcommentary = random.randint(0,1)
                else:
                    rngcommentary = 0
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
            if tobool(options_dict["adverts"]) == True:
                play("advert")
            else:
                continue

    main()

except KeyboardInterrupt:
    log("main", "Keyboard interrupt detected, closing...")
    print("Goodbye!")
    exit(0)
