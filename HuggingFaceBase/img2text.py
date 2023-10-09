from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import requests
import os
# import streamlit as st


load_dotenv(find_dotenv())      # to be able to access hugging face api key stored in .env
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")



# https://huggingface.co/tasks


# https://huggingface.co/tasks/image-to-text
# img2text
def img2text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    
    text = image_to_text(url)[0]['generated_text']
    
    print(text)
    return text

img2text("London_panorama.jpg")