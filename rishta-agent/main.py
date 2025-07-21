from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool 
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
import asyncio
import chainlit as cl
from whatsapp import whatsapp_message

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client=external_client   
)

@function_tool
def get_user_data(min_age: int) -> list[dict]:
    "Retrieve user data baed on a mininmum age"
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Raza", "age": 19},
        {"name": "Ali", "age": 20},
        {"name": "Fatima", "age": 18},
        {"name": "Zehra", "age": 21},
        {"name": "Zainab", "age": 20},
        {"name": "Zara", "age": 19},
        {"name": "Sakina", "age": 18}

    ]

    for user in users:
        if user["age"] < min_age:
            users.remove(user)
    
    return users

rishte_wali_agent = Agent(
    name="Aunty",
    instructions="You are a warm and wise 'rishte wali aunty' who helps people find the perfect match for them and send whatsapp messages only if user asks. Dont ask bout the gender, use your intellegence to detect it and if the user is male then only show female rishta and vice verca. in response, give a table including the names of opposite gender only with their ages. In the end ask if they want these details on their whatsapp? if yes then send it immediately using ultramsg api which is integrated. Replace 'naam' and 'umar' with 'name' and 'age'",
    model=model,
    tools=[get_user_data, whatsapp_message]
)
 

# @cl.on_chat_resume
# async def start():
#     await cl.Message("Salam beta! Rishte wali aunty here. Tell me your name, age and whatsapp number").send()


@cl.on_message
async def main(message: cl.Message):
    await cl.Message("Thinking...").send()
    history = cl.user_session.get("history") or []
    # greeted = cl.user_session.get("greeting") or False
    # history.append({"role": "user", "content": message.content})


    if len(history) == 0:

        await cl.Message("Salam beta! Rishte wali aunty here. Tell me your name, age and whatsapp number").send()
        history.append({"role":"user", "content": message.content})
        cl.user_session.set("history", history)

        return

    history.append({"role":"user", "content": message.content})


    for h in history:
        print(h)

    response = Runner.run_sync(
        starting_agent=rishte_wali_agent,
        input=history
    )

    history.append({"role":"assistant", "content": response.final_output})

    cl.user_session.set("history", history)

    await cl.Message(content = response.final_output).send()
