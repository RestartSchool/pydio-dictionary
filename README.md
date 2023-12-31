# Pydio
## Before You Run...
When you run the program, you will be asked to use either Interactive Setup or a Config File to start Pydio. Please use Interactive Setup, the config file has not been implemented yet!

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
