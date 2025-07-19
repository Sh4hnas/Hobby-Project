# Voice Assistant (ALEXA) - API Documentation

A Python-based voice assistant that can respond to voice commands, perform web searches, tell jokes, play music, and engage in AI-powered conversations using Google's Gemini AI.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Public API Reference](#public-api-reference)
- [Usage Examples](#usage-examples)
- [Voice Commands](#voice-commands)
- [Dependencies](#dependencies)
- [Error Handling](#error-handling)

## Installation

### Prerequisites

- Python 3.7 or higher
- Microphone for voice input
- Internet connection for AI features

### Required Dependencies

```bash
pip install pyttsx3 speechrecognition pyjokes google-generativeai pyaudio
```

**Note**: On Linux, you may need to install additional system packages:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

## Configuration

### Google Gemini AI Setup

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the API key in the code:
```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```

### Audio Configuration

The assistant uses your system's default microphone. Ensure your microphone is working and has proper permissions.

## Public API Reference

### Core Functions

#### `sptext()`

**Description**: Captures and converts speech input to text using Google's speech recognition service.

**Parameters**: None

**Returns**: 
- `str`: Recognized speech text in lowercase
- `None`: If speech recognition fails or times out

**Exceptions**:
- `sr.UnknownValueError`: When speech cannot be understood
- `sr.WaitTimeoutError`: When listening times out (5 second limit)

**Example**:
```python
user_input = sptext()
if user_input:
    print(f"User said: {user_input}")
```

---

#### `speechtx(x)`

**Description**: Converts text to speech using the pyttsx3 text-to-speech engine.

**Parameters**:
- `x` (str): Text to be spoken

**Returns**: None

**Configuration**:
- Voice: Uses first available system voice (typically female)
- Speech Rate: 150 words per minute

**Example**:
```python
speechtx("Hello, how can I help you today?")
```

---

#### `ai_chat(prompt)`

**Description**: Generates AI responses using Google's Gemini Pro model.

**Parameters**:
- `prompt` (str): User's question or statement to process

**Returns**:
- `str`: AI-generated response text
- `str`: Error message if API call fails

**Example**:
```python
response = ai_chat("What is the weather like today?")
print(response)
speechtx(response)
```

## Usage Examples

### Basic Voice Assistant Loop

```python
# Start the voice assistant
if __name__ == '__main__':
    while True:
        # Listen for user input
        user_input = sptext()
        
        if user_input:
            # Process commands or use AI chat
            if "exit" in user_input:
                speechtx("Goodbye!")
                break
            else:
                response = ai_chat(user_input)
                speechtx(response)
```

### Custom Command Integration

```python
def handle_custom_command(user_input):
    """Add your own custom commands here"""
    if "weather" in user_input:
        speechtx("Let me check the weather for you")
        # Add weather API integration
    elif "calendar" in user_input:
        speechtx("Opening your calendar")
        # Add calendar functionality
    else:
        # Fall back to AI chat
        response = ai_chat(user_input)
        speechtx(response)

# Usage
user_input = sptext()
if user_input:
    handle_custom_command(user_input)
```

### Error Handling Example

```python
def safe_voice_interaction():
    """Example of robust voice interaction with error handling"""
    try:
        user_input = sptext()
        if user_input:
            response = ai_chat(user_input)
            speechtx(response)
        else:
            speechtx("I didn't catch that. Please try again.")
    except Exception as e:
        print(f"Error in voice interaction: {e}")
        speechtx("Sorry, there was an error. Please try again.")
```

## Voice Commands

The assistant recognizes the following built-in voice commands:

### Information Commands

| Command | Response | Example |
|---------|----------|---------|
| "your name" | States assistant name | "My name is ALEXA" |
| "age" | States assistant age | "I am 4 years old" |
| "time" | Current time | "Current time is 3:45 PM" |

### Action Commands

| Command | Action | Notes |
|---------|--------|-------|
| "youtube" | Opens YouTube | Uses default browser |
| "joke" | Tells a random joke | Uses pyjokes library |
| "song" | Plays music | Requires local music directory setup |
| "exit" or "quit" | Terminates assistant | Graceful shutdown |

### AI Chat

Any command not matching the above patterns will be sent to Google Gemini AI for processing.

**Examples**:
- "What is the capital of France?"
- "Tell me a story about dragons"
- "Help me write an email"
- "Explain quantum physics"

## Dependencies

### Core Libraries

```python
import pyttsx3              # Text-to-speech conversion
import speech_recognition   # Speech-to-text conversion  
import datetime            # Date and time operations
import webbrowser          # Web browser control
import pyjokes             # Joke generation
import os                  # Operating system interface
import google.generativeai # Google Gemini AI integration
```

### Dependency Details

- **pyttsx3**: Offline text-to-speech library
- **speech_recognition**: Google Speech Recognition API wrapper
- **datetime**: Built-in Python datetime handling
- **webbrowser**: Built-in web browser control
- **pyjokes**: Random joke generator
- **os**: Built-in operating system interface
- **google.generativeai**: Google's Gemini AI client library

## Error Handling

### Speech Recognition Errors

```python
# The sptext() function handles these automatically:
try:
    audio = recognizer.listen(source, timeout=5)
    data = recognizer.recognize_google(audio)
    return data.lower()
except sr.UnknownValueError:
    print("Not Understanding!!!")
    return None
except sr.WaitTimeoutError:
    print("Listening timed out.")
    return None
```

### AI Chat Errors

```python
# The ai_chat() function includes error handling:
try:
    response = model.generate_content(prompt)
    return response.text
except Exception as e:
    print("Gemini Error:", e)
    return "Sorry, I couldn't answer that."
```

### Music Playback Errors

```python
# Song playback includes error handling:
try:
    songs = os.listdir(music_directory)
    os.startfile(os.path.join(music_directory, songs[0]))
    speechtx("Playing song")
except Exception as e:
    print("Song error:", e)
    speechtx("Sorry, I couldn't play the song.")
```

## Configuration Options

### Voice Settings

Modify voice properties in the `speechtx()` function:

```python
def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Voice selection (0 = first voice, 1 = second voice, etc.)
    engine.setProperty('voice', voices[0].id)  
    
    # Speech rate (words per minute)
    engine.setProperty('rate', 150)  # Adjust between 100-200
    
    # Volume level (0.0 to 1.0)
    engine.setProperty('volume', 1.0)
    
    engine.say(x)
    engine.runAndWait()
```

### Music Directory Setup

For the song command to work, update the music directory path:

```python
# Windows example:
music_directory = r'C:\Users\YourUsername\Music'

# Linux/Mac example:
music_directory = '/home/username/Music'
# or
music_directory = '~/Music'
```

## Security Considerations

1. **API Key Security**: Never commit your Google Gemini API key to version control
2. **Environment Variables**: Use environment variables for sensitive data:

```python
import os
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
```

3. **Microphone Permissions**: Ensure your application has proper microphone permissions

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**: Install missing dependencies
2. **"No module named 'pyaudio'"**: Install system audio libraries
3. **"API key error"**: Verify your Gemini API key is valid
4. **"Microphone not working"**: Check system microphone permissions
5. **"Speech not recognized"**: Ensure clear speech and good microphone quality

### Debug Mode

Enable debug output by adding print statements:

```python
def debug_sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        # ... rest of function
```

## License

This project is provided as-is for educational and personal use.

---

*Generated documentation for Voice Assistant (ALEXA) - Version 1.0*
