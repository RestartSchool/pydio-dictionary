# Pydio
# Made with ❤️ by Restart
# 2023-2024

try:
    # Define dicts
    options_dict = {}
    paths_dict = {}

    # ------ Get Working Path ------
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
        # If user input is Yes, convert to True bool
        if (user == True) or (user.lower() == "y") or (user.lower() == "true"):
            return True
        # If it's anything else, convert to False bool
        else:
            return False

    # ------ Interactive Setup - Option Y/N Function ------
    def optionyn(question, default):
        # Make our question string
        user = str(input(f"{question} ({default}) (y/n)>")).lower()
        # If yes, use tobool function to convert to True bool
        if user == "y":
            return tobool(user)
        # If no, use tobool function to convert to False bool
        elif user == "n":
            return tobool(user)
        # If invalid answer, use default answer from function
        else:
            print("Invalid option, using default option.")
            return default

    # ------ Interactive Setup - Option Path Function ------
    def optionpath(question, default):
        # Ask Make our question string
        user = str(input(f"{question} >"))
        # Decide if path is valid
        if os.path.isdir(user):
            # Make backslashes compliant with Windows Pathing
            # This is hardcoded to Windows and might not work on Linux / macOS
            user = user.replace("\\", "\\\\")
            print(user)
            return user
        else:
            # Make backslashes compliant with Windows Pathing
            # This is hardcoded to Windows and might not work on Linux / macOS
            print("Path selected is invalid, using default path.")
            default = default.replace("\\", "\\\\")
            print(default)
            return default

    # ------ Interactive Setup ------
    def InteractiveSetup():
        global options_dict, paths_dict

        #Ask questions, add answers to relevant dict / dict key
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
        #Make dicts global
        global options_dict, paths_dict

        # Set up reader
        import configparser
        config = configparser.RawConfigParser()

        # Read options section of config file, add it to dict
        try:
            config.read(path)
            options_dict = dict(config.items('OPTIONS'))
        except Exception as error:
            log("init", "Config file error: Error while reading Options section! The file may be missing or malformed. Calling error handler...")
            errorhandler("init", error)

        # Read path section of config file, add it to dict
        try:
            config.read(path)
            paths_dict = dict(config.items('PATHS'))
        except Exception as error:
            log("init", "Config file malformed: Error while reading Paths section! The file may be missing or malformed. Calling error handler...")
            errorhandler("init", error)


    # ------ Setup Handoff ------
    option = int(input("Please select an option:\n1: Use Interactive Setup\n2. Use Config File\n> "))
    while True:
        if option == 1:
            InteractiveSetup()
            break
        elif option == 2:
            # Hardcoded path, need to change this
            readconfigfile("config.cfg")
            break
        else:
            print("Invalid option!")

    # ------ Imports ------
    try:
        # Load required functions
        import pygame # Pygame - Audio
        import random # Random - Random Values
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
    # Music files are always searched as are mandatory for Pydio to function
    log("init", "Detecting music files...")
    musicfiles = os.listdir(paths_dict['musicpath'])
    log("init", f"Music detection complete, {len(musicfiles)} music files detected.")
    # Commentary Files
    # If commentary is disabled, we don't bother trying to search for them
    if tobool(options_dict["commentary"]) == True:
        log("init", "Detecting commentary files...")
        commentaryfiles = os.listdir(paths_dict['commentarypath'])
        log("init", f"Commentary detection complete, {len(commentaryfiles)} commentary files detected.")
    # Advert Files
    # If adverts are disabled, we don't bother trying to search for them
    if tobool(options_dict["adverts"]) == True:
        log("init", "Detecting advert files...")
        advertfiles = os.listdir(paths_dict['advertpath'])
        log("init", f"Advert detection complete, {len(advertfiles)} advert files detected.")

    log("init", "Init complete! Handing over to main function.\n")

    # Write Overview to Logs
    log("main", f"Welcome! Overview:\nIndents Activated? {options_dict['indent']}\nSong Announce TTS Activated? {options_dict['songannounce']}\nCommentary Activated? {options_dict['commentary']}\nAdverts Activated? {options_dict['adverts']}\n")
    log("main", f"Path Information:\nRunning Path: {path}\nPath Slash Type: {pathtype}\nMusic Path: {paths_dict['musicpath']}\nMusic Path: {paths_dict['commentarypath']}\nMusic Path: {paths_dict['advertpath']}\n")

    # ------ Reference: TTS - Announcement Locations -----
    # 1 = before song
    # 2 = start of song
    # 3 = end of song
    # 4 = after song
    # 5 = none

    # ------ TTS Function ------
    def tts(metadata, position):
        # Make engine global, may try to find a better way to do this
        global engine

        # Start engine
        engine = pyttsx3.init()
        # WIP - Pick voice, currently hardcoded but the user may have a choice soon
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        # If there are multiple artists, separate them with "and"
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
        # List of speech options
        songannouncebefore = [f"Here's {artist} with {metadata['title']}", f"Now, {metadata['title']} by {artist}", f"Now, {artist} with {metadata['title']}", f"Here's {metadata['title']} by {artist}"]
        songannounceafter = [f"That was {artist} with {metadata['title']}", f"You just heard {metadata['title']} by {artist}", f"That was the voice of {artist} with {metadata['title']}", f"You just heard {metadata['title']} by {artist}"]

        # Decide positions and speech option, then load up the speech
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
        
        # The following code is a mess and is in the process of being rewritten :)
        
        # Decide song announcements
        if tobool(options_dict["songannounce"]) == True:
            announcelocation = random.randint(2,2)
        else:
            announcelocation = 5
        
        # Log
        log("song", f"Location for song announcement is: {announcelocation}. Starting song {song}...")

        # Set up Song Player and Volume
        sound = pygame.mixer.Sound(song)
        volume = 1
        sound.set_volume(volume)
        
        # Announcement Location Decision Tree
        if announcelocation == 1:
            # --- Before Song TTS ---
            
            # --- TTS ---
            # Read metadata
            audio = EasyID3(song)
            
            # Set up TTS
            tts(audio, "before")
            log("tts", f"Generated TTS in pos {announcelocation}.")
            log("tts", f"Playing TTS.")
            
            # Run TTS
            engine.runAndWait()

            # --- Music ---
            # Start music
            channel = sound.play()
            if tobool(options_dict["songannounce"])  == True:
                # No need to read metadata as it was already read by TTS
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")

            # --- Delay ---
            # Wait for song to complete...
            if tobool(options_dict["testmode"]) == False:
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()

        elif announcelocation == 2:
            # --- Start of Song TTS ---
            
            # --- Music ---
            # Start music
            channel = sound.play()
            if tobool(options_dict["songannounce"])  == True:
                audio = EasyID3(song)
                print(audio)
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")
            
            # --- TTS ---
            # Generate TTS
            tts(audio, "before")
            log("tts", f"Generated TTS in pos {announcelocation}. Waiting for location...")
            
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
            
            # --- Delay ---
            # Wait for song to complete...
            if tobool(options_dict["testmode"]) == False:
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()
            
            # Song complete, log it
            log("song", "Song complete.")
        
        elif announcelocation == 3:
            # End of Song TTS
            
            # --- Music ---
            # Start music
            channel = sound.play()
            if tobool(options_dict["songannounce"])  == True:
                audio = EasyID3(song)
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")
            
            # --- Delay ---
            # Wait until 20 seconds remaining - not working
            if tobool(options_dict["testmode"]) == False:
                print(channel.get_length())
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()

            # --- TTS ---
            # Generate TTS
            tts(audio, "before")
            log("tts", f"Generated TTS in pos {announcelocation}. Waiting for location...")
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
        
        elif announcelocation == 4:
            # --- After Song TTS ---

            # --- TTS ---
            # Read metadata
            audio = EasyID3(song)

            # --- Music ---
            # Start music
            channel = sound.play()
            if tobool(options_dict["songannounce"])  == True:
                # No need to read metadata as it was already read by TTS
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")

            # --- Delay ---
            # Wait for song to complete...
            if tobool(options_dict["testmode"]) == False:
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()

            # --- TTS ---
            # Read metadata
            audio = EasyID3(song)
            
            # Set up TTS
            tts(audio, "before")
            log("tts", f"Generated TTS in pos {announcelocation}.")
            log("tts", f"Playing TTS.")
            
            # Run TTS
            engine.runAndWait()
        
        elif announcelocation == 5:
            # --- No TTS ---
            
            # --- Music ---
            # Start music
            channel = sound.play()
            if tobool(options_dict["songannounce"])  == True:
                audio = EasyID3(song)
                log("song", f"Song {audio['title']} by {audio['artist']} is playing...")
            else:
                log("song", f"Song {song} is playing...")
            
            # --- Delay ---
            # Wait for song to complete...
            if tobool(options_dict["testmode"]) == False:
                while channel.get_busy() == True:
                    time.sleep(0.5)
            else:
                time.sleep(5)
                channel.stop()
            
            # Song complete, log it
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
            # Decide amount of songs to play before rolling adverts
            if len(musicfiles) >= 4:
                rngtriggeradvert = random.randint(2,4)
            else:
                rngtriggeradvert = len(musicfiles)
            if tobool(options_dict["adverts"]) == True:
                log("main", f"RNG has decided {rngtriggeradvert} songs will be played before adverts!")
            else:
                log("main", f"Adverts are disabled.")
            # Song loop
            for i in range(0, rngtriggeradvert):
                # Decide whether or not to play commentary
                if tobool(options_dict["commentary"]) == True:
                    rngcommentary = random.randint(0,1)
                else:
                    rngcommentary = 0
                # Run code based on commentary
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
            # Play advert if enabled
            if tobool(options_dict["adverts"]) == True:
                play("advert")
            else:
                continue

    main()

# Detect keyboard interrupt and exit cleanly
except KeyboardInterrupt:
    log("main", "Keyboard interrupt detected, closing...")
    print("Goodbye!")
    exit(0)
