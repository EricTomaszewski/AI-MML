# AutoGen with Local LLMs | Get Rid of OpenAI API Keys >>> LM Studio
# https://youtu.be/xa5irTrK5n4?si=Q4JS3woCg7KCFvbi

# Local LLM on Runpod
# https://www.youtube.com/watch?v=wp0xSHmZjBQ



import os
import autogen
# TO LOAD OpenAI Key
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())      # to be able to access OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo-16k'

config_list = [
    {
        'model': MODEL,
        'api_key': OPENAI_API_KEY
    }
]

# FOR LM Studio Inference API (or in other words - Endpoint)
"""config_list = [
    {
        'api_type': 'open_ai',
        'api_base': 'http://localhost:1234/v1',
        'api_key': 'NULL'
    }
]"""


llm_config = {'config_list': config_list}

# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0.5,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)


# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)


# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message=r"""
    What is the height of Eiffel Tower?
    """,
)



# message =
#    Write a potem about the beautiful sunny weather.
#    Don't use any code - just write a poem.



#message=r
# Read this word file with that has this absolute path 'C:\Users\irene\!AI-LLM\AutoGenCV\coding\2023-10 - CV Eric TOMASZEWSKI.doc'
# Keep the text as it is but change the font to Arial.
# Save the file to the working directory and name it 'Amended.doc'



# message=
"""
Read a Word file from the current working directory "coding"
Write a function to print numbers 1 to 10 and make sure to save it to Word file. 
Save the code & Word file to disc, bearing in mind that it is running on Windows (use only Windows compatible libraries).
"""

# Write Each message as a consecutive Step. For example - the first message should be named STEP 1, the second STEP 2 and so on.