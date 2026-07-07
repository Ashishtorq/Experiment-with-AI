import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

load_dotenv()

my_groq_api = os.getenv('GROQ_API_KEY')


if not my_groq_api:
    raise ValueError('api is wrong')

client = Groq(api_key = my_groq_api)

model = 'llama-3.3-70b-versatile'
role = 'user'
prompt = 'who is Virat Kohli'

message={
    'role':role, 
    'content':prompt
}

messages = [message]

response = client.chat.completions.create(model = model, messages = messages)

print(response)


print('######################################')

print(response.choices[0].message.content)

