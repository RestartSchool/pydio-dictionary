# Pydio
## Before You Run...
Pydio is currently not in a state to be easily used. It uses several hard coded options and paths. Here's my file structure that may work for you:\
├── music\
│   └── music files here\
├── commentary\
│   └── commentary files here\
├── advert\
│   └── advert files here\
├── logs\
│   └── logs will appear here\
└── main.py\
If you use that file/folder layout on Windows, the program should work OK.
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

`m4a` is NOT supported.
Read more at the Pygame mixer docs: https://www.pygame.org/docs/ref/mixer.html

## Dependencies
- Pygame - handles audio
- Mutagen - handles MP3 metadata
- PYTTSX3 - Handles TTS

These dependencies can be installed using Pip, or your Python package manager of choice.
### Install Dependencies Command - Pip
`pip install pygame mutagen pyttsx3`
