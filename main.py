import speech_recognition as sr
import webbrowser  
import datetime  
import wikipedia 
import os
from modules import takeCommand, clean_query, extract_video_and_platform, tellTime, open_application, app_aliases, open_file , extract_news_topic , get_news_summary
from gemini_chat import ConversationMemory, chat_with_gemini



# === Logging Setup ===
LOG_FILE_PATH = "assistant_log.txt"

def log_to_file(text):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        f.write(f"{timestamp}{text}\n")

# Initialize conversation memory
history = ConversationMemory(max_turns=5)

def say(text):
    log_to_file(f"Assistant: {text}")
    os.system(f'say "{text}"')  

def greet(name="Sir"):
    now = datetime.datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 22:
        greeting = "Good evening"
    else:
        greeting = "Hello"

    say(f"{greeting} {name}")

# === Main Program ===
if __name__ == '__main__':
    greet()
    app_keywords = [f"open {alias.lower()}" for alias in app_aliases.keys()]
    while True:
        query = takeCommand()
        if not query:
            continue
        query = query.lower().strip()
        log_to_file(f"User: {query}")

        if "youtube" in query.lower():
            if "search" in query.lower() or "play" in query.lower():
                try:
                    video, platform = extract_video_and_platform(query)
                    say(f'Searching "{video}" on "{platform}"')
                    url = f'https://www.youtube.com/results?search_query={video}'
                    webbrowser.open(url, new=0, autoraise=True)
                except Exception as e:
                    say("Sorry, I couldn't process your YouTube request.")
                    log_to_file(f"❌ YouTube Parsing Error: {e}")
            else:
                webbrowser.open('https://www.youtube.com', new=0, autoraise=True)
                say("Opening YouTube")
            continue

        elif "wikipedia" in query:
            try:
                say("Checking Wikipedia")
                topic, _ = extract_video_and_platform(query)
                result = wikipedia.summary(topic, sentences=3)
                log_to_file(f"Wikipedia Result: {result}")
                say("According to Wikipedia")
                say(result)
            except wikipedia.exceptions.DisambiguationError as e:
                say("The topic is ambiguous. Please be more specific.")
                log_to_file(f"Wikipedia Disambiguation Options: {e.options}")
            except Exception as e:
                say("Sorry, I couldn't find anything on Wikipedia.")
                log_to_file(f"❌ Wikipedia Error: {e}")
            continue
                
        if "google" in query.lower():
            if "search" in query.lower() or "in google".lower():
                try:
                    content, platform = extract_video_and_platform(query)
                    say(f'Searching "{content}" on Google')
                    url = f'https://www.google.com/search?q={content}'
                    webbrowser.open(url, new=0, autoraise=True)
                except Exception as e:
                    say("Sorry, I couldn't process your Google search request.")
                    log_to_file(f"❌ Google Parsing Error: {e}")
            else:
                webbrowser.open('https://www.google.com', new=0, autoraise=True)
                say("Opening Google")
            continue

        elif "your name" in query:
            say("I am Luna, your desktop Assistant.")
            continue
        
        elif "bye" in query or "exit" in query:
            say("Okay, see you again!")
            open('assistant_log.txt', 'w').close()
            break
        
        elif "time now" in query or "what is the time now" in query:
            say(tellTime())
            continue
        
        elif "open" in query.lower() and any(kw in clean_query(query) for kw in app_keywords):
            open_application(query)
            continue

        elif "find file" in query or "search file" in query:
            file = clean_query(query)
            open_file(file)
            continue
        
        elif "open" in query.lower():
            try:
                content = query.replace("open", "")
                say(f'Searching "{content}" on Google')
                url = f'https://www.google.com/search?q={content}'
                webbrowser.open(url, new=0, autoraise=True)
            except Exception as e:
                say("Sorry, I couldn't process your request.")
                log_to_file(f"❌ Google Parsing Error: {e}")
        elif "news" in query.lower() or "headline" in query.lower() or "headlines" in query.lower():
            topic = extract_news_topic(query)
            summary = get_news_summary(topic)
            say("Here are the latest headlines:")
            say(summary)
            log_to_file(summary)
            continue

        else:
            if query == " " or query == "" or query == None or query =="none":
                say("i did not understand")
            else:
                query = clean_query(query)
                response, history = chat_with_gemini(query, history)
                log_to_file(f"Gemini: {response}")
                say(response)
