# Pydio
***An Automatic Radio System, built in Python3***
## Setup
### Using Config File
Using the config file allows you to setup Pydio once, and not have to set it up again. I have provided a template config file, `config-to-edit.cfg`, where you can configure the options and paths to your liking.\
\
Once you have configured the config file, you can use the config file by renaming it to `config.cfg`, run Pydio and select **Config File** when prompted.

### Using Interactive Setup
You can use Interactive Setup to create a config for Pydio in a more user friendly way. When starting Pydio, select **Interactive Setup** when prompted. Then, follow the steps to configure Pydio.

## Compatibility
### Operating Systems
- Windows: ✅️
- macOS: Not Tested
- Linux: Not Tested
- Replit: ❌️ - Replit does not support audio playback through Pygame

Pydio was built on Python 3.12 using Windows 11. It should work on most recent versions of Python 3.

### File Formats
Pydio supports most mainstream file formats through Pygame.
Examples:
- `mp3`
- `wav`
- `flac`
- `ogg`

`m4a` is NOT supported.\
Read more about Pygame Mixer at the Pygame mixer docs: https://www.pygame.org/docs/ref/mixer.html

## Dependencies
- Pygame (https://github.com/pygame/pygame) - handles audio
- Mutagen (https://github.com/quodlibet/mutagen) - handles MP3 metadata
- PYTTSX3 (https://github.com/nateshmbhat/pyttsx3) - Handles TTS

These dependencies can be installed using Pip, or your Python package manager of choice.
### Install Dependencies Command - Pip
`pip install pygame mutagen pyttsx3`
