import os
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
from pydantic import BaseModel
import json

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


class Tickets(BaseModel):
    name: str
    age: int
    address: str
    product: str
    price: str
    issue: str


schema = Tickets.model_json_schema()

responses_format = {"type": "json_object"}

system_prompt = f"""
        I want personal information from this text that should be strictly based on this schema and give me json output.
        {schema} 
"""
complain = "My name is ashish singh. I live in delhi, and my age is 16 and I am pursuing B.Tech. I purchased i phone 17. Now this is not working. I have to exchange product or get full refund"
prompt = f""" 
        This is user's complain from you need to extract user's personal information from this text {complain}
"""


system_message = {"role": "system", "content": system_prompt}
client = Groq(api_key=groq_api_key)
model = "llama-3.3-70b-versatile"
role = "user"
message = {"role": role, "content": prompt}

messages = [system_message, message]

response = client.chat.completions.create(
    model=model, messages=messages, response_format=responses_format
)

print(response.choices[0].message.content)

raw_json = response.choices[0].message.content

res = json.loads(raw_json)
ticket = Tickets(**res)
print("###############")
print(ticket.name)
print(ticket.age)
print(ticket.name)