import chainlit as cl
from openai import OpenAI
import os

os.environ['OPENAI_API_KEY'] = ""
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
@cl.on_message
async def main(message : str):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role":"assistant" ,"content":"you are a helpful assistant"},
            {"role":"user" ,"content":message.content}
        ],
        temperature = 1,
    )
    await cl.Message(content = f"{response.choices[0].message.content}",).send()
