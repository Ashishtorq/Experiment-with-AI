import os 
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path 

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key = groq_api_key)
prompt = 'Suggest name for my food company'
model = 'llama-3.3-70b-versatile'
role = 'system'

message = {
    "role" : "user",
    "content" : prompt
}

message_system = {
    "role" : "system",
    "content" : "You are brand manager, who suggest name for my food company, name should be one worded and suggest only one word"
}
messages = [message, message_system]

response = client.chat.completions.create( model=model, messages=messages, temperature=2)

print(response.choices[0].message.content)

