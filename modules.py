import speech_recognition as sr
import spacy
import datetime
import os
import subprocess
import requests
from sk import NEWS_API_KEY



def find_folder(foldername, search_path="/Users/user_name"):
    matches = []
    for root, dirs, files in os.walk(search_path):
        for dir in dirs:
            if foldername.lower() in dir.lower():
                matches.append(os.path.join(root, dir))
    return matches

def open_path(path):
    subprocess.run(["open", path])

def open_file(query):
    cleaned = clean_query(query)
    if "find file" in cleaned or "search file" in cleaned:
        filename = cleaned.replace("find file", "").replace("search file", "").strip()
        results = find_folder(filename)
        if results:
            print("Found files:")
            for i, file_path in enumerate(results[:5], 1):
                print(f"{i}. {file_path}")
            open_path(results[0])
        else:
            print("No matching files found.")

app_aliases = {
    "chrome": "Google Chrome",
    "google": "Google Chrome",
    "safari": "Safari",
    "notes": "Notes",
    "vscode": "Visual Studio Code",
    "vs code": "Visual Studio Code",
    "code": "Visual Studio Code",
    "terminal": "Terminal",
    "settings": "System Settings",
    "system preferences": "System Preferences",
    "spotify": "Spotify",
    "music": "Music",
    "brave": "Brave Browser",
    "canva": "Canva",
    "chatgpt": "ChatGPT",
    "citrix": "Citrix Workspace",
    "cursor": "Cursor",
    "firefox": "Firefox",
    "google chrome": "Google Chrome",
    "keynote": "Keynote",
    "pages": "Pages",
    "parsec": "Parsec",
    "prime video": "Prime Video",
    "telegram": "Telegram",
    "unsplash": "Unsplash Wallpapers",
    "whatsapp": "WhatsApp",
    "imovie": "iMovie",
    "zoom": "zoom.us",
    "numbers": "Numbers",
    "microsoft excel": "Microsoft Excel",
    "excel": "Microsoft Excel",
    "microsoft powerpoint": "Microsoft PowerPoint",
    "powerpoint": "Microsoft PowerPoint",
    "microsoft word": "Microsoft Word",
    "word": "Microsoft Word",
    "onedrive": "OneDrive",
    "flipclock": "flipclock"
}


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='en-in')
            print("User =", Query)
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
        return Query

nlp = spacy.load("en_core_web_sm")

def clean_query(query, assistant_name="luna"):
    query = query.lower().strip().replace(",", "")
    query = query.replace("from ai", " ")
    query = query.replace("using ai", " ")
    wake_words = [f"hey {assistant_name}", f"okay {assistant_name}", f"ok {assistant_name}"]
    for wake_word in wake_words:
        if query.startswith(wake_word):
            query = query[len(wake_word):].strip()
            break
    return query


def extract_video_and_platform(query):
    query = clean_query(query)
    doc = nlp(query)
    video = ""
    platform = ""
    for token in doc:
        if token.text in ["on", "in", "from"]:
            if token.i + 1 < len(doc):
                platform = doc[token.i + 1:].text.strip()
            video = doc[:token.i].text.replace("play", "").replace("search for", "").strip()
            break
    return video.strip(), platform.capitalize()

import re

def extract_news_topic(query):
    query = clean_query(query)
    patterns = [
        r"(tell me|what's|latest|any)?\s*(news|headlines|updates)?\s*(about|on|in)?\s*",  # generic
        r"^news\s*", 
    ]
    for pattern in patterns:
        query = re.sub(pattern, "", query, flags=re.IGNORECASE).strip()
        
    return query if query else "technology"

def tellTime():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]
    return f'The time is {hour} Hours and {min} Minutes'

def open_application(query):
    query = clean_query(query)
    if query.startswith("open"):
        app_requested = query.replace("open", "", 1).strip()
        app_to_open = app_aliases.get(app_requested, app_requested.title())
        try:
            os.system(f"open -a '{app_to_open}'")
            print(f"✅ Opening {app_to_open}")
            return f"✅ Opening {app_to_open}"
        except Exception as e:
            print(f"❌ Couldn't open {app_to_open}: {e}")
    else:
        print("❌ Not an app-opening command.")



def get_news_summary(topic="general"):
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=en&pageSize=3"
        response = requests.get(url)
        articles = response.json()["articles"]

        if not articles:
            return f"No news found for {topic}."

        summaries = []
        for i, article in enumerate(articles):
            summaries.append(f"{i+1}. {article['title']} - {article['source']['name']}")

        return "\n".join(summaries)
    except Exception as e:
        return f"Error fetching news: {e}"
