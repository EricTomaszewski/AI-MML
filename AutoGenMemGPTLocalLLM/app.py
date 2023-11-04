# AutoGEN + MemGPT + Local LLM (Complete Tutorial) 😍
# https://www.youtube.com/watch?v=bMWXXPoDnDs

# pip install openai pyautogen pymemgpt >>> they do NOT install correctly on Python 3.12! Go for e.g. 3.11.2
# pip show {package}

import os
import autogen
import memgpt.autogen.memgpt_agent as memgpt_autogen
import memgpt.autogen.interface as autogen_interface
import memgpt.agent as agent
import memgpt.system as system
import memgpt.utils as utils
import memgpt.presets as presets
import memgpt.constants as constants
import memgpt.personas.personas as personas
import memgpt.humans.humans as humans
from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithEmbeddings, InMemoryStateManagerWithFaiss
import openai


config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:8000/v1",
        "api_key": "NULL",
        "read_timeout": 300,
        "max_retries": 10,
        "temperature": 0.1,
    }
]

llm_config = {"config_list": config_list, "seed": 42}


# If USE_MEMGPT is False, then this example will be the same as the official AutoGen repo
# https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb
# If USE_MEMGPT is True, then we swap out the "coder" agent with MemGPT Agent

USE_MEMGPT = False


# api keyds for the MemGPT to work
openai.api_base = "http://localhost:8000/v1"
openai.api_key = "NULL"


# The user agent
user_proxy = autogen.UserProxyAgent(
    name = "User_proxy",
    system_message = "A human admin",
    code_execution_config = {"last_n_message": 2, "work_dir": "groupchat"},
    human_input_mode = "TERMINATE",
    default_auto_reply = "You are going to figure all out by your own."
    "Work by yourself, the user won't reply until you output 'TERMINATE' to end the conversation.",
)

interface = autogen_interface.AutoGenInterface()
persistence_manager = InMemoryStateManager()
persona = "I am a 10x engineer, trained in Python. I was the first engineer at Uber."
human = "I am a team manager at this company"
memgpt_agent = presets.use_preset(presets.DEFAULT_PRESET, model='gpt-4', persona=persona, human=human, interface=interface, persistence_manager=persistence_manager, agent_config=llm_config)


if not USE_MEMGPT:
    # In the AugoGen example, we create an AssistantAgent to play the role of the coder
    coder = autogen.AssistantAgent(
        name = "Coder",
        llm_config = llm_config,
        system_message = f"I am a 10x engineer, trained in Python. I was the first engineer at Uber",
        human_input_mode = "TERMINATE",
    )
else:
    # In our example, we swap this AutoGen agent with a MemGPT agent
    # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
    print("\nMemGPT Agent at work\n")
    coder = memgpt_autogen.MemGPTAgent(
        name = "MemGPT_coder",
        agent = memgpt_agent,
    )
    

# Beging the group chat with a message from the user
user_proxy.initiate_chat(
    coder,
    message = "Write a function to print number 1 to 10 in Python"
