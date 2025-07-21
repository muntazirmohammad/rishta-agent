import chainlit as cl
from agents import function_tool
import requests
import os

@function_tool
def whatsapp_message(number: str, message: str):
    
    instance_id = os.getenv("INSTANCE_ID")
    api_token = os.getenv("API_TOKEN")

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    payload = {
        "token": api_token,
        "to": number,
        "body": message
    }

    response = requests.post(url,data=payload)

    if response.status_code == 200:
        return f"Message sent successfully to {number}"
    else: 
        return f"Failed to send message. Error: {response.text}"
    
    