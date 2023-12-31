# TO RUN:
# streamlit run app.py

# https://huggingface.co/tasks


# TO LOAD HuggingFace API Token + OpenAI Key
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())      # to be able to access hugging face api key stored in .env
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


import requests
# from transformers import pipeline           # for HuggingFace task 1 but doesn't work in this script => but on Colab - YES


# Imports for 2. LLM to create the story.
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.llms import OpenAI             # depreciated >>> use the one below instead
from langchain.chat_models import ChatOpenAI


# Imports for 4. Streamlit web app interface
import streamlit as st


# ============================================


# 1. Image2Text
# HuggingFace => "Interference API"
def img2text(filename):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]


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

    return story


# ============================================


# 3. text to speech
# https://huggingface.co/tasks/text-to-speech
# https://huggingface.co/espnet/kan-bayashi_ljspeech_vits
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


# ============================================


# 4. Streamlit web app interface
def main():
    st.set_page_config(page_title="img 2 audio story", page_icon="O")
    
    st.header("Turn img into audio story")    
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    
    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)
        st.image(uploaded_file, caption="Uploaded Image.",
                 use_column_width=True)
        scenario = img2text(uploaded_file.name)
        story = generate_story(scenario)
        text2speech(story)
        
        with st.expander("scenario"):
            st.write(scenario)
        with st.expander("story"):
            st.write(story)
            
        st.audio("audio.flac")
        
        
if __name__ == "__main__":
    main()