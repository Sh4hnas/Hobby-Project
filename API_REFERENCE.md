# API Reference - Voice Assistant

This document provides detailed technical documentation for all public APIs, functions, and components in the Voice Assistant project.

## Module Overview

The voice assistant is implemented in `project1.py` and provides three core functions for speech processing and AI interaction.

## Function Reference

### Speech Recognition Functions

#### `sptext()`

```python
def sptext() -> Optional[str]
```

**Purpose**: Captures audio from the microphone and converts it to text using Google's Speech Recognition API.

**Technical Details**:
- Uses `speech_recognition.Recognizer()` with Google Web Speech API
- Automatically adjusts for ambient noise before listening
- 5-second timeout for audio capture
- Returns lowercase text for consistent processing

**Return Values**:
- `str`: Successfully recognized speech in lowercase
- `None`: Recognition failed, timed out, or audio was unclear

**Error Handling**:
- `sr.UnknownValueError`: Audio was captured but speech was not intelligible
- `sr.WaitTimeoutError`: No speech detected within 5-second timeout
- All exceptions are caught and handled gracefully

**Implementation Notes**:
- Requires active internet connection for Google Speech API
- Microphone access permissions required
- Ambient noise adjustment improves recognition accuracy

**Example Usage**:
```python
# Basic usage
text = sptext()
if text:
    print(f"Recognized: {text}")

# With error handling
try:
    text = sptext()
    if text is not None:
        process_command(text)
    else:
        print("No speech detected or recognition failed")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

### Text-to-Speech Functions

#### `speechtx(x)`

```python
def speechtx(x: str) -> None
```

**Purpose**: Converts text input to audible speech using the pyttsx3 text-to-speech engine.

**Parameters**:
- `x` (str): Text string to be converted to speech

**Technical Details**:
- Uses offline TTS engine (no internet required)
- Configured with first available system voice
- Speech rate set to 150 words per minute
- Blocks execution until speech is complete

**Voice Configuration**:
- **Voice**: `voices[0].id` (typically default female voice)
- **Rate**: 150 WPM (configurable)
- **Volume**: System default

**Platform Compatibility**:
- **Windows**: Uses SAPI5
- **macOS**: Uses NSSpeechSynthesizer  
- **Linux**: Uses espeak

**Example Usage**:
```python
# Basic text-to-speech
speechtx("Hello, how can I help you?")

# Dynamic content
current_time = datetime.now().strftime("%I:%M %p")
speechtx(f"The current time is {current_time}")

# Error messages
try:
    risky_operation()
except Exception:
    speechtx("An error occurred. Please try again.")
```

---

### AI Integration Functions

#### `ai_chat(prompt)`

```python
def ai_chat(prompt: str) -> str
```

**Purpose**: Generates intelligent responses using Google's Gemini Pro AI model.

**Parameters**:
- `prompt` (str): User's question, statement, or conversation input

**Return Values**:
- `str`: AI-generated response text
- `str`: Error message if API call fails ("Sorry, I couldn't answer that.")

**Technical Details**:
- Uses Google Gemini Pro model (`gemini-pro`)
- Requires valid Google AI API key
- Handles rate limiting and API errors gracefully
- No conversation history maintained (stateless)

**API Configuration**:
```python
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="models/gemini-pro")
```

**Error Handling**:
- Network connectivity issues
- API quota exceeded
- Invalid API key
- Malformed requests
- Service unavailable

**Example Usage**:
```python
# Simple question answering
response = ai_chat("What is the capital of France?")
print(response)  # "The capital of France is Paris."

# Complex queries
response = ai_chat("Explain quantum computing in simple terms")
speechtx(response)

# Error handling
response = ai_chat("Tell me a joke")
if "Sorry, I couldn't" not in response:
    speechtx(response)
else:
    speechtx("I'm having trouble connecting to AI services")
```

## Command Processing Logic

### Built-in Commands

The main application loop processes voice input through pattern matching:

```python
if "your name" in data1:
    speechtx("My name is ALEXA")
elif "age" in data1:
    speechtx("I am 4 years old")
elif "time" in data1:
    time = datetime.datetime.now().strftime("%I:%M %p")
    speechtx("Current time is " + time)
# ... more commands
```

### Command Categories

#### Information Commands
- **Name Query**: `"your name"` → Identity response
- **Age Query**: `"age"` → Age response  
- **Time Query**: `"time"` → Current time

#### Action Commands
- **Web Navigation**: `"youtube"` → Opens YouTube in browser
- **Entertainment**: `"joke"` → Tells random joke
- **Media Control**: `"song"` → Plays local music file
- **Exit Commands**: `"exit"` or `"quit"` → Graceful shutdown

#### Fallback Processing
- Any unmatched input is sent to `ai_chat()` for intelligent response

## Configuration Parameters

### Speech Recognition Settings

```python
# Microphone configuration
recognizer = sr.Recognizer()
recognizer.adjust_for_ambient_noise(source)  # Auto noise adjustment
audio = recognizer.listen(source, timeout=5)  # 5-second timeout
```

### Text-to-Speech Settings

```python
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)    # Voice selection
engine.setProperty('rate', 150)              # Speech rate (WPM)
```

### AI Model Settings

```python
model = genai.GenerativeModel(model_name="models/gemini-pro")
# Available models: gemini-pro, gemini-pro-vision (for images)
```

## Error Codes and Messages

### Speech Recognition Errors

| Error Type | Message | Cause |
|------------|---------|-------|
| `UnknownValueError` | "Not Understanding!!!" | Speech unclear or background noise |
| `WaitTimeoutError` | "Listening timed out." | No speech detected in 5 seconds |
| `RequestError` | Connection error | No internet or API unavailable |

### AI Chat Errors

| Error Type | Response | Cause |
|------------|----------|-------|
| `Exception` | "Sorry, I couldn't answer that." | API error, quota exceeded, or network issue |

### Media Playback Errors

| Error Type | Message | Cause |
|------------|---------|-------|
| `FileNotFoundError` | "Song error: [details]" | Music directory not found |
| `PermissionError` | "Song error: [details]" | File access denied |
| `OSError` | "Song error: [details]" | File format not supported |

## Performance Considerations

### Response Times
- **Speech Recognition**: 1-3 seconds (network dependent)
- **Text-to-Speech**: Immediate (offline processing)
- **AI Chat**: 2-5 seconds (API dependent)

### Resource Usage
- **Memory**: ~50MB base + model loading
- **CPU**: Low (except during audio processing)
- **Network**: Required for speech recognition and AI features

### Optimization Tips
1. Use environment variables for API keys
2. Implement connection pooling for repeated AI requests
3. Cache common responses to reduce API calls
4. Use local TTS voices for faster speech synthesis

## Security Best Practices

### API Key Management
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=api_key)
```

### Input Validation
```python
def safe_ai_chat(prompt: str) -> str:
    if not isinstance(prompt, str):
        return "Invalid input type"
    if len(prompt.strip()) == 0:
        return "Empty prompt provided"
    if len(prompt) > 1000:  # Limit prompt length
        return "Prompt too long"
    return ai_chat(prompt)
```

### Microphone Privacy
- Request explicit user permission for microphone access
- Provide visual indicators when listening
- Allow users to mute/disable voice features

## Testing and Debugging

### Unit Testing Examples

```python
import unittest
from unittest.mock import patch, MagicMock

class TestVoiceAssistant(unittest.TestCase):
    
    @patch('speech_recognition.Recognizer')
    def test_sptext_success(self, mock_recognizer):
        # Mock successful speech recognition
        mock_recognizer.return_value.recognize_google.return_value = "Hello"
        result = sptext()
        self.assertEqual(result, "hello")
    
    @patch('pyttsx3.init')
    def test_speechtx(self, mock_init):
        # Mock TTS engine
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        speechtx("test message")
        mock_engine.say.assert_called_with("test message")
        mock_engine.runAndWait.assert_called_once()
```

### Debug Mode Implementation

```python
DEBUG = True

def debug_log(message: str):
    if DEBUG:
        print(f"[DEBUG] {datetime.now()}: {message}")

def sptext_debug():
    debug_log("Starting speech recognition")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        debug_log("Adjusting for ambient noise")
        recognizer.adjust_for_ambient_noise(source)
        debug_log("Listening for speech")
        # ... rest of function with debug statements
```

## Integration Examples

### Custom Command Extension

```python
def register_custom_command(keyword: str, handler_func):
    """Register a new voice command"""
    custom_commands[keyword] = handler_func

def weather_handler(user_input: str):
    """Handle weather-related queries"""
    # Integrate with weather API
    weather_data = get_weather_data()
    response = f"Current weather: {weather_data['description']}, {weather_data['temperature']}°F"
    speechtx(response)

# Register the command
register_custom_command("weather", weather_handler)
```

### Multi-language Support

```python
def set_language(lang_code: str):
    """Configure language settings"""
    # Speech recognition language
    recognizer.recognize_google(audio, language=lang_code)
    
    # TTS language (if supported)
    voices = engine.getProperty('voices')
    for voice in voices:
        if lang_code in voice.id:
            engine.setProperty('voice', voice.id)
            break
```

---

*API Reference for Voice Assistant - Version 1.0*
*Last Updated: $(date)*