# https://huggingface.co/tasks

# TO LOAD HuggingFace API Token + OpenAI Key
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())      # to be able to access hugging face api key stored in .env
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


import requests
from transformers import pipeline           # for HuggingFace but doesn't work in this script => but on Colab - YES


# Imports for 2. LLM to create the story.
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.llms import OpenAI             # depreciated >>> use the one below instead
from langchain.chat_models import ChatOpenAI


# ============================================


# 1. Image2Text
# HuggingFace => "Interference API"
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
print(headers)

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]

output = query("London_panorama.jpg")
print(output)
print("")



# WORKS ON COLAB BUT NOT IN VS Code Studio
# COLAB: https://colab.research.google.com/drive/1pmbNDGKS6e2egVhvf6GdFyKetKBi-epl#scrollTo=goR5q0bDiHXo
# HuggingFace => "Use in Transformers"
# Use a pipeline as a high-level helper
'''from transformers import pipeline

def img2text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    
    text = image_to_text(url)[0]['generated_text']
    
    # print(text)
    return text
    
img2text("London_panorama.jpg")'''


# ============================================


# 2. LLM to create the story.
# https://huggingface.co/tasks/text-generation
def generate_story(scenario):
    template = """
    You are a story teller:
    You can generate a short story based on a simple narrative, the story should be no more than 20 words;
    
    CONTEXT: {scenario}
    STORY:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    
    story_llm = LLMChain(llm=ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=1), prompt=prompt, verbose=True
                         )
    
    story = story_llm.predict(scenario=scenario)
    
    print("")
    print(story)
    print("")
    return story


message = generate_story(output)


# ============================================


# https://huggingface.co/tasks/text-to-speech
# https://huggingface.co/espnet/kan-bayashi_ljspeech_vits
# 3. text to speech
def text2speech(message):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    payloads = {
        "inputs": message
    }
    
    response = requests.post(API_URL, headers=headers, json=payloads)
    with open('audio.flac', 'wb') as file:
        file.write(response.content)
        
    print("")
    print("Finished creating an audio file: audio.flac")
    print("")
        
text2speech(message)