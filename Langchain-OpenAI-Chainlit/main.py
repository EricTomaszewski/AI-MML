# https://www.youtube.com/watch?v=xZDB1naRUlk

# TO RUN
# chainlit run main.py -w
# -w => chainlit to watch for changes and restart web app automatically

'''
LIMITATIONS:
1. No streaming.
2. No "generating" messages
3. No backend context.
and that's why we need LANGCHAIN
'''

import chainlit as cl
import openai
import os

# os.environ['OPENAI_API_KEY'] = ''
# return everything that the user inputs


# pass the message into chatgpt api. .send() the answer.


@cl.on_message
async def main(message : str):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {'role': 'assistant', 'content': 'you are a helpful assistant'},
            {'role': 'user', 'content': message}
        ],
        temperature = 1,
    )
    # await cl.Message(content=message).send()
    # await cl.Message(content=str(response)).send()
    await cl.Message(content=response['choices'][0]['message']['content']).send()
    # await cl.Message(content=f"{response['choices'][0]['message']['content']}").send()
