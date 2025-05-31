import google.generativeai as genai
import os
from sk import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ConversationMemory:
    def __init__(self, max_turns=5):
        self.max_turns = max_turns  
        self.history = []  

    def add_user_message(self, message):
        self.history.append(("user", message))
        self._truncate()

    def add_assistant_message(self, message):
        self.history.append(("assistant", message))
        self._truncate()

    def _truncate(self):
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_messages_for_gemini(self):
        messages = []
        for role, msg in self.history:
            api_role = "model" if role == "assistant" else "user"
            messages.append({"role": api_role, "parts": [msg]})
        return messages

    def clear(self):
        self.history = []

def chat_with_gemini(query, memory):
    # Add instruction for short answers directly in user query
    query = query + " Please answer short if the question is general or detailed if you think question is related to programming "
    memory.add_user_message(query)
    
    messages = memory.get_messages_for_gemini()
    
    # Do NOT add system messages — API rejects 'system' role
    # messages.insert(0, system_message)  <-- remove this
    
    try:
        response = model.generate_content(messages)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Error: {e}"
        
    memory.add_assistant_message(reply)
    
    
    return reply, memory



