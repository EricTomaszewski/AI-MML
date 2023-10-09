# TO RUN:
# streamlit run app.py

from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain import PromptTemplate, LLMChain, OpenAI
import requests
import os
import streamlit as st


load_dotenv(find_dotenv())      # to be able to access hugging face api key stored in .env
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")



# https://huggingface.co/tasks


# https://huggingface.co/tasks/image-to-text
# https://huggingface.co/Salesforce/blip-image-captioning-base
# img2text
def img2text(url):
    # TO DOWNLOAD MODELS AND USE LOCALLY
    # BUT A BETTER OPTION IS USING "Inference API"
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    
    text = image_to_text(url)[0]['generated_text']
    
    print(text)
    

    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": "Bearer {HUGGINGFACEHUB_API_TOKEN}"}

    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()

    output = query("cats.jpg")
    
    return text

img2text("London_panorama.jpg")



# https://huggingface.co/tasks/text-generation
# llm
def generate_story(scenario):
    template = """
    You are a story teller:
    You can generate a short story based on a simple narrative, the story should be no more than 20 words;
    
    CONTEXT: {scenario}
    STORY:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    
    story_llm = LLMChain(llm=OpenAI(
        model_name="gpt-3.5-turbo", temperature=1), prompt=prompt, verbose=True
                         )
    
    story = story_llm.predict(scenario=scenario)
    
    print(story)
    return story



# https://huggingface.co/tasks/text-to-speech
# https://huggingface.co/espnet/kan-bayashi_ljspeech_vits
# text to speech
def text2speech(message):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": "Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    payloads = {
        "inputs": message
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    with open('audio.flac', 'wb') as file:
        file.write(response.content)
    
    
    
   ''' 
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": "The answer to the universe is 42",
    })'''
    
    
    
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