import os 
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path 

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key = groq_api_key)
prompt = 'what is computer science'
model = 'llama-3.3-70b-versatile'
role = 'user'

message = {
    "role" : role,
    "content" : prompt
}

messages = [message]

response = client.chat.completions.create( model=model, messages=messages)

print(response.choices[0].message.content)

