# Usage Examples and Implementation Guide

This document provides practical examples and implementation patterns for using the Voice Assistant APIs effectively.

## Quick Start Examples

### Basic Voice Assistant Setup

```python
#!/usr/bin/env python3
"""
Basic Voice Assistant Implementation
Run this script to start a simple voice assistant
"""
import os
from project1 import sptext, speechtx, ai_chat

def main():
    """Main voice assistant loop with basic error handling"""
    speechtx("Voice assistant starting up. Say something!")
    
    while True:
        try:
            # Listen for user input
            user_input = sptext()
            
            if user_input is None:
                continue
                
            print(f"User said: {user_input}")
            
            # Handle exit commands
            if any(word in user_input for word in ["exit", "quit", "goodbye", "stop"]):
                speechtx("Goodbye! Have a great day!")
                break
                
            # Process with AI
            response = ai_chat(user_input)
            print(f"Assistant: {response}")
            speechtx(response)
            
        except KeyboardInterrupt:
            speechtx("Voice assistant shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")
            speechtx("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    main()
```

### Environment Setup Example

```python
"""
Secure Voice Assistant with Environment Variables
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from project1 import sptext, speechtx

# Load environment variables
load_dotenv()

def setup_ai():
    """Configure AI with environment variables"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY environment variable")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def secure_ai_chat(model, prompt):
    """AI chat with input validation"""
    if not prompt or len(prompt.strip()) == 0:
        return "I didn't understand. Could you please repeat that?"
    
    if len(prompt) > 1000:
        return "That's quite a long question. Could you make it shorter?"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble processing that right now."

# Usage
model = setup_ai()
user_input = sptext()
if user_input:
    response = secure_ai_chat(model, user_input)
    speechtx(response)
```

## Advanced Implementation Patterns

### Command Router Pattern

```python
"""
Advanced Command Router Implementation
"""
import re
from datetime import datetime
from typing import Dict, Callable, Optional
from project1 import sptext, speechtx, ai_chat

class VoiceCommandRouter:
    """Route voice commands to appropriate handlers"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.patterns: Dict[str, Callable] = {}
        
    def register_command(self, keyword: str, handler: Callable):
        """Register a simple keyword-based command"""
        self.commands[keyword.lower()] = handler
        
    def register_pattern(self, pattern: str, handler: Callable):
        """Register a regex pattern-based command"""
        self.patterns[pattern] = handler
        
    def process_input(self, user_input: str) -> bool:
        """Process user input and route to appropriate handler"""
        user_input = user_input.lower().strip()
        
        # Check simple keyword commands
        for keyword, handler in self.commands.items():
            if keyword in user_input:
                handler(user_input)
                return True
                
        # Check pattern-based commands
        for pattern, handler in self.patterns.items():
            if re.search(pattern, user_input):
                handler(user_input)
                return True
                
        return False  # No command matched

# Example usage
router = VoiceCommandRouter()

# Register simple commands
def tell_time(user_input: str):
    current_time = datetime.now().strftime("%I:%M %p")
    speechtx(f"The current time is {current_time}")

def tell_joke(user_input: str):
    import pyjokes
    joke = pyjokes.get_joke()
    speechtx(joke)

router.register_command("time", tell_time)
router.register_command("joke", tell_joke)

# Register pattern-based commands
def set_reminder(user_input: str):
    # Extract reminder text using regex
    match = re.search(r"remind me to (.+)", user_input)
    if match:
        reminder_text = match.group(1)
        speechtx(f"I'll remind you to {reminder_text}")
        # Add reminder logic here
    else:
        speechtx("What would you like me to remind you about?")

router.register_pattern(r"remind me to", set_reminder)

# Main loop
def main():
    speechtx("Advanced voice assistant ready!")
    
    while True:
        user_input = sptext()
        if user_input:
            if "exit" in user_input:
                speechtx("Goodbye!")
                break
                
            # Try to route the command
            if not router.process_input(user_input):
                # Fall back to AI chat
                response = ai_chat(user_input)
                speechtx(response)
```

### Context-Aware Assistant

```python
"""
Context-Aware Voice Assistant
Maintains conversation context and user preferences
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from project1 import sptext, speechtx, ai_chat

@dataclass
class ConversationContext:
    """Store conversation context and user preferences"""
    user_name: Optional[str] = None
    conversation_history: List[str] = None
    last_topic: Optional[str] = None
    preferences: dict = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.preferences is None:
            self.preferences = {}

class ContextualAssistant:
    """Voice assistant with context awareness"""
    
    def __init__(self):
        self.context = ConversationContext()
        
    def add_to_history(self, user_input: str, response: str):
        """Add interaction to conversation history"""
        timestamp = datetime.now().strftime("%H:%M")
        self.context.conversation_history.append(f"[{timestamp}] User: {user_input}")
        self.context.conversation_history.append(f"[{timestamp}] Assistant: {response}")
        
        # Keep only last 10 interactions
        if len(self.context.conversation_history) > 20:
            self.context.conversation_history = self.context.conversation_history[-20:]
            
    def get_contextual_prompt(self, user_input: str) -> str:
        """Create AI prompt with context"""
        base_prompt = f"User said: {user_input}\n"
        
        if self.context.user_name:
            base_prompt += f"User's name is {self.context.user_name}.\n"
            
        if self.context.last_topic:
            base_prompt += f"Previous topic was about {self.context.last_topic}.\n"
            
        if self.context.conversation_history:
            recent_history = "\n".join(self.context.conversation_history[-4:])
            base_prompt += f"Recent conversation:\n{recent_history}\n"
            
        base_prompt += "Please respond naturally and reference previous context if relevant."
        return base_prompt
        
    def process_input(self, user_input: str) -> str:
        """Process input with context awareness"""
        # Check for name introduction
        if "my name is" in user_input.lower():
            name_match = user_input.lower().split("my name is")
            if len(name_match) > 1:
                self.context.user_name = name_match[1].strip().title()
                response = f"Nice to meet you, {self.context.user_name}!"
                self.add_to_history(user_input, response)
                return response
                
        # Generate contextual response
        contextual_prompt = self.get_contextual_prompt(user_input)
        response = ai_chat(contextual_prompt)
        
        # Extract topic for context
        if len(user_input.split()) > 3:
            self.context.last_topic = user_input[:50] + "..." if len(user_input) > 50 else user_input
            
        self.add_to_history(user_input, response)
        return response

# Usage example
assistant = ContextualAssistant()

def main():
    speechtx("Hello! I'm your contextual assistant. What's your name?")
    
    while True:
        user_input = sptext()
        if user_input:
            if "exit" in user_input:
                name_part = f", {assistant.context.user_name}" if assistant.context.user_name else ""
                speechtx(f"Goodbye{name_part}! It was nice talking with you.")
                break
                
            response = assistant.process_input(user_input)
            speechtx(response)

if __name__ == "__main__":
    main()
```

## Integration Examples

### Web API Integration

```python
"""
Voice Assistant with Web API Integration
"""
import requests
from project1 import sptext, speechtx, ai_chat

class WebIntegratedAssistant:
    """Assistant with web service integrations"""
    
    def __init__(self):
        self.weather_api_key = "YOUR_WEATHER_API_KEY"
        self.news_api_key = "YOUR_NEWS_API_KEY"
        
    def get_weather(self, city: str = "London") -> str:
        """Get weather information"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"Weather in {city}: {temp}°C, {description}"
            else:
                return f"Sorry, I couldn't get weather for {city}"
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return "Sorry, weather service is unavailable"
            
    def get_news(self, topic: str = "technology") -> str:
        """Get latest news"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': topic,
                'apiKey': self.news_api_key,
                'pageSize': 3,
                'sortBy': 'publishedAt'
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if response.status_code == 200 and data['articles']:
                headlines = []
                for article in data['articles'][:3]:
                    headlines.append(article['title'])
                return f"Latest {topic} news: " + ". ".join(headlines)
            else:
                return f"Sorry, no news found for {topic}"
                
        except Exception as e:
            print(f"News API error: {e}")
            return "Sorry, news service is unavailable"
            
    def process_command(self, user_input: str) -> str:
        """Process commands with web integration"""
        user_input = user_input.lower()
        
        if "weather" in user_input:
            # Extract city if mentioned
            words = user_input.split()
            if "in" in words:
                try:
                    city_index = words.index("in") + 1
                    city = words[city_index] if city_index < len(words) else "London"
                    return self.get_weather(city.title())
                except:
                    return self.get_weather()
            return self.get_weather()
            
        elif "news" in user_input:
            # Extract topic if mentioned
            if "about" in user_input:
                topic_part = user_input.split("about")[-1].strip()
                return self.get_news(topic_part)
            return self.get_news()
            
        else:
            # Fall back to AI chat
            return ai_chat(user_input)

# Usage
assistant = WebIntegratedAssistant()

def main():
    speechtx("Web-integrated assistant ready! Ask about weather or news.")
    
    while True:
        user_input = sptext()
        if user_input:
            if "exit" in user_input:
                speechtx("Goodbye!")
                break
                
            response = assistant.process_command(user_input)
            print(f"Response: {response}")
            speechtx(response)

if __name__ == "__main__":
    main()
```

### GUI Integration with Tkinter

```python
"""
Voice Assistant with GUI Interface
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from project1 import sptext, speechtx, ai_chat

class VoiceAssistantGUI:
    """GUI interface for voice assistant"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("600x500")
        
        self.is_listening = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Conversation display
        self.conversation = scrolledtext.ScrolledText(
            main_frame, 
            width=70, 
            height=20,
            state='disabled'
        )
        self.conversation.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Input field
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=50)
        input_entry.grid(row=1, column=0, padx=(0, 5))
        input_entry.bind('<Return>', self.send_text)
        
        # Send button
        send_btn = ttk.Button(main_frame, text="Send", command=self.send_text)
        send_btn.grid(row=1, column=1, padx=(0, 5))
        
        # Voice button
        self.voice_btn = ttk.Button(
            main_frame, 
            text="🎤 Listen", 
            command=self.toggle_voice
        )
        self.voice_btn.grid(row=1, column=2)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
    def add_to_conversation(self, speaker: str, message: str):
        """Add message to conversation display"""
        self.conversation.config(state='normal')
        self.conversation.insert(tk.END, f"{speaker}: {message}\n\n")
        self.conversation.config(state='disabled')
        self.conversation.see(tk.END)
        
    def send_text(self, event=None):
        """Send text input to AI"""
        text = self.input_var.get().strip()
        if not text:
            return
            
        self.input_var.set("")
        self.add_to_conversation("You", text)
        
        # Process in background thread
        threading.Thread(target=self.process_text, args=(text,), daemon=True).start()
        
    def process_text(self, text: str):
        """Process text input"""
        self.status_var.set("Processing...")
        
        try:
            response = ai_chat(text)
            self.add_to_conversation("Assistant", response)
            
            # Speak response in background
            threading.Thread(target=speechtx, args=(response,), daemon=True).start()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.add_to_conversation("System", error_msg)
            
        finally:
            self.status_var.set("Ready")
            
    def toggle_voice(self):
        """Toggle voice listening"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
            
    def start_listening(self):
        """Start voice listening"""
        self.is_listening = True
        self.voice_btn.config(text="🔴 Stop")
        self.status_var.set("Listening...")
        
        # Listen in background thread
        threading.Thread(target=self.voice_listen_loop, daemon=True).start()
        
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_btn.config(text="🎤 Listen")
        self.status_var.set("Ready")
        
    def voice_listen_loop(self):
        """Voice listening loop"""
        while self.is_listening:
            try:
                user_input = sptext()
                if user_input and self.is_listening:
                    self.add_to_conversation("You (voice)", user_input)
                    self.process_text(user_input)
                    
            except Exception as e:
                if self.is_listening:
                    self.add_to_conversation("System", f"Voice error: {str(e)}")
                    
        self.status_var.set("Ready")

# Usage
def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

## Testing Examples

### Unit Tests

```python
"""
Unit Tests for Voice Assistant Functions
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestVoiceAssistant(unittest.TestCase):
    """Test cases for voice assistant functions"""
    
    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_sptext_success(self, mock_mic, mock_recognizer):
        """Test successful speech recognition"""
        # Mock the recognizer
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "Hello World"
        
        # Import and test
        from project1 import sptext
        result = sptext()
        
        self.assertEqual(result, "hello world")
        
    @patch('speech_recognition.Recognizer')
    def test_sptext_timeout(self, mock_recognizer):
        """Test speech recognition timeout"""
        import speech_recognition as sr
        
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.listen.side_effect = sr.WaitTimeoutError()
        
        from project1 import sptext
        result = sptext()
        
        self.assertIsNone(result)
        
    @patch('pyttsx3.init')
    def test_speechtx(self, mock_init):
        """Test text-to-speech function"""
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        
        from project1 import speechtx
        speechtx("Test message")
        
        mock_engine.say.assert_called_with("Test message")
        mock_engine.runAndWait.assert_called_once()
        
    @patch('google.generativeai.GenerativeModel')
    def test_ai_chat_success(self, mock_model):
        """Test successful AI chat"""
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        
        mock_response = MagicMock()
        mock_response.text = "AI response"
        mock_model_instance.generate_content.return_value = mock_response
        
        from project1 import ai_chat
        result = ai_chat("Test prompt")
        
        self.assertEqual(result, "AI response")
        
    @patch('google.generativeai.GenerativeModel')
    def test_ai_chat_error(self, mock_model):
        """Test AI chat error handling"""
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        
        from project1 import ai_chat
        result = ai_chat("Test prompt")
        
        self.assertEqual(result, "Sorry, I couldn't answer that.")

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
"""
Integration Tests for Voice Assistant
"""
import unittest
from unittest.mock import patch
import time
import threading

class TestVoiceAssistantIntegration(unittest.TestCase):
    """Integration tests for complete voice assistant workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.responses = []
        
    def mock_speechtx(self, text):
        """Mock speech output for testing"""
        self.responses.append(text)
        
    @patch('project1.speechtx')
    @patch('project1.sptext')
    @patch('project1.ai_chat')
    def test_complete_interaction_flow(self, mock_ai, mock_sptext, mock_speechtx):
        """Test complete user interaction flow"""
        # Setup mocks
        mock_sptext.return_value = "hello"
        mock_ai.return_value = "Hello! How can I help you?"
        mock_speechtx.side_effect = self.mock_speechtx
        
        # Import and run main logic simulation
        from project1 import sptext, speechtx, ai_chat
        
        user_input = sptext()
        if user_input:
            response = ai_chat(user_input)
            speechtx(response)
            
        # Verify the flow
        mock_sptext.assert_called_once()
        mock_ai.assert_called_once_with("hello")
        self.assertIn("Hello! How can I help you?", self.responses)
        
    @patch('project1.speechtx')
    @patch('project1.sptext')
    def test_command_recognition(self, mock_sptext, mock_speechtx):
        """Test built-in command recognition"""
        mock_speechtx.side_effect = self.mock_speechtx
        
        test_commands = [
            ("your name", "My name is ALEXA"),
            ("age", "I am 4 years old"),
            ("time", "Current time is"),  # Partial match due to dynamic time
        ]
        
        for command, expected_response in test_commands:
            with self.subTest(command=command):
                mock_sptext.return_value = command
                self.responses.clear()
                
                # Simulate command processing
                from project1 import sptext, speechtx
                import datetime
                
                user_input = sptext()
                if "your name" in user_input:
                    speechtx("My name is ALEXA")
                elif "age" in user_input:
                    speechtx("I am 4 years old")
                elif "time" in user_input:
                    time_str = datetime.datetime.now().strftime("%I:%M %p")
                    speechtx("Current time is " + time_str)
                    
                # Check if expected response is in the actual response
                self.assertTrue(any(expected_response in resp for resp in self.responses),
                              f"Expected '{expected_response}' not found in {self.responses}")

if __name__ == '__main__':
    unittest.main()
```

## Performance Optimization Examples

### Caching and Performance

```python
"""
Performance-Optimized Voice Assistant
"""
import functools
import time
from typing import Dict, Any
from project1 import sptext, speechtx, ai_chat

class PerformanceOptimizedAssistant:
    """Voice assistant with performance optimizations"""
    
    def __init__(self):
        self.response_cache: Dict[str, str] = {}
        self.cache_timeout = 300  # 5 minutes
        self.cache_timestamps: Dict[str, float] = {}
        
    @functools.lru_cache(maxsize=100)
    def cached_ai_response(self, prompt: str) -> str:
        """Cache AI responses for common queries"""
        return ai_chat(prompt)
        
    def get_cached_response(self, prompt: str) -> str:
        """Get response with time-based caching"""
        current_time = time.time()
        
        # Check if we have a cached response
        if prompt in self.response_cache:
            cache_time = self.cache_timestamps.get(prompt, 0)
            if current_time - cache_time < self.cache_timeout:
                return self.response_cache[prompt]
                
        # Get new response and cache it
        response = ai_chat(prompt)
        self.response_cache[prompt] = response
        self.cache_timestamps[prompt] = current_time
        
        return response
        
    def preload_common_responses(self):
        """Preload responses for common queries"""
        common_queries = [
            "hello",
            "how are you",
            "what can you do",
            "help",
            "goodbye"
        ]
        
        for query in common_queries:
            self.cached_ai_response(query)
            
    def batch_process_inputs(self, inputs: list) -> list:
        """Process multiple inputs efficiently"""
        responses = []
        for user_input in inputs:
            response = self.get_cached_response(user_input)
            responses.append(response)
        return responses

# Usage example
assistant = PerformanceOptimizedAssistant()
assistant.preload_common_responses()

# Process user input with caching
user_input = sptext()
if user_input:
    response = assistant.get_cached_response(user_input)
    speechtx(response)
```

## Error Handling and Logging

```python
"""
Robust Error Handling and Logging
"""
import logging
import traceback
from datetime import datetime
from project1 import sptext, speechtx, ai_chat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RobustVoiceAssistant:
    """Voice assistant with comprehensive error handling"""
    
    def __init__(self):
        self.error_count = 0
        self.max_errors = 5
        
    def safe_sptext(self) -> str:
        """Speech recognition with error handling"""
        try:
            result = sptext()
            if result:
                logger.info(f"Speech recognized: {result}")
                return result
            else:
                logger.warning("No speech recognized")
                return None
                
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            logger.debug(traceback.format_exc())
            self.error_count += 1
            return None
            
    def safe_speechtx(self, text: str) -> bool:
        """Text-to-speech with error handling"""
        try:
            speechtx(text)
            logger.info(f"Speech output: {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            logger.debug(traceback.format_exc())
            self.error_count += 1
            return False
            
    def safe_ai_chat(self, prompt: str) -> str:
        """AI chat with error handling"""
        try:
            response = ai_chat(prompt)
            logger.info(f"AI response generated for: {prompt[:30]}...")
            return response
            
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            logger.debug(traceback.format_exc())
            self.error_count += 1
            return "I'm sorry, I'm having trouble processing that right now."
            
    def check_system_health(self) -> bool:
        """Check if system is healthy"""
        if self.error_count >= self.max_errors:
            logger.critical(f"Too many errors ({self.error_count}). System may be unstable.")
            return False
        return True
        
    def reset_error_count(self):
        """Reset error counter"""
        self.error_count = 0
        logger.info("Error count reset")
        
    def run(self):
        """Main application loop with error handling"""
        logger.info("Voice assistant starting")
        self.safe_speechtx("Voice assistant starting up!")
        
        while True:
            try:
                if not self.check_system_health():
                    self.safe_speechtx("System experiencing issues. Restarting...")
                    self.reset_error_count()
                    continue
                    
                user_input = self.safe_sptext()
                
                if user_input is None:
                    continue
                    
                if "exit" in user_input.lower():
                    self.safe_speechtx("Goodbye!")
                    logger.info("User requested exit")
                    break
                    
                response = self.safe_ai_chat(user_input)
                self.safe_speechtx(response)
                
                # Reset error count on successful interaction
                if self.error_count > 0:
                    self.error_count = max(0, self.error_count - 1)
                    
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                self.safe_speechtx("Shutting down...")
                break
                
            except Exception as e:
                logger.critical(f"Unexpected error in main loop: {e}")
                logger.debug(traceback.format_exc())
                self.error_count += 1
                
                if self.check_system_health():
                    self.safe_speechtx("I encountered an error but I'm still running.")
                else:
                    logger.critical("System unstable, shutting down")
                    break
                    
        logger.info("Voice assistant shutting down")

# Usage
if __name__ == "__main__":
    assistant = RobustVoiceAssistant()
    assistant.run()
```

---

*Usage Examples and Implementation Guide for Voice Assistant - Version 1.0*
*This document provides practical examples for implementing and extending the voice assistant functionality.*