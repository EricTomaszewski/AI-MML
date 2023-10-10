# streamlit run app.py

import os
from dotenv import load_dotenv      # to get API keys from .env

from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests
import json
# import streamlit as st
from langchain.schema import SystemMessage
from fastapi import FastAPI

load_dotenv()
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")



# 1. Tool for search. >>> Search for useful links.
# https://serper.dev/
# COMPARISON OF VARIOUS Google Search APIs (most cost effective are Google ones):
# https://python.langchain.com/docs/integrations/tools/search_tools
def search(query):
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query
    })
    
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    
    return response.text

# it is also possible to do it directly with langchain (rather than using serper.dev):
# https://python.langchain.com/docs/integrations/tools/google_search 
# https://python.langchain.com/docs/integrations/tools/google_serper

# search("What is meta's thread product?")
print()


# 2. Tool for scraping.
# https://www.browserless.io/ 
def scrape_website(objective: str, url: str):
    # scrape website, and also will summarize the content based on objective if the content...
    # objective is the original objective & task that user give to the agent, url is the url...
    
    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }
    
    # Define the data to be sent in the request
    data = {
        "url": url
    }
    
    # Revert Python object to JSON string
    data_json = json.dumps(data)
    
    # Send the POST request
    post_url = f"https://chrome.browserless.io/content?token={browserless_api_key}"
    response = requests.post(post_url, headers=headers, data=data_json)
    
    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENTTTTT:", text)
        if len(text) > 10000:
            output = summary(objective,text)
            return output
        else:
            return text
        # return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")
        
#scrape_website("what is langchain?", "https://python.langchain.com/en/latest/index.html")



# How to handle LLM token limit?
# 1. Summary - Map reduce => for less amount of data.
# 2. Vector search - search for relevant content => for huge amount of data.
# >>> for this demo => Summary
def summary(objective, content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
    
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chink_size=10000, chunk_overlap=500      # cut into number of arrays of 10000 tokens each
    )
    docs = text_splitter.create_documents([content])            # create an array of all those chunks
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"]
    )
    
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,         # prompt to summarize each chunk
        combine_prompt = map_prompt_template    # combine summary for each paragraph into one paragraph
    )
    
    output = summary_chain.run(input_documents=docs, objective=objective)
    
    return output



class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape website"""
    objective: str = Field(description="The objective & task that user gives to the agent")
    url: str = Field(description="The url of the website to be scraped")


        
class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT "
    args_schema: type[BaseModel] = ScrapeWebsiteInput
    
    def _run(self, objective: str, url: str):
        return scrape_website(objective, url)
    
    def _arun(self, url: str):
        raise NotImplementedError("error here")
        



# 3. Create langchain agent with the tools above.
tools = [
    Tool(
        name = "Search",
        func = search,
        description = "useful for when you need to answer questions about current events, data. You should ask targeted questions"
    ),
    ScrapeWebsiteTool(),
]

system_message = SystemMessage(
    content = """You are a world class researcher, who can do detailed research on any topic and produce facts based results;
    you do not make things up, you will try as hard as possible to gather facts & data to back up research
    
    Please make sure you complete the objective above with the following rules:
    1/ You should do enough research to gather as much information as possible about the objective
    2/ If there are url or relevant links & articles, you will scrape it to gather more information
    3/ After scraping & search, you should think "is there any new things I should search & scrape based on the data I collected to increase research quality?" If answer is yes, continue; But don't do this more than 3 iterations
    4/ You should not make things up, you should only write facts & data that you have gathered
    5/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & link to back up your research
    6/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & link to back up your research
    """
)

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
memory = ConversationSummaryBufferMemory(memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)



# streamlit run app.py
# 4. Use streamlit to create a web app
# https://streamlit.io/
'''def main():
    st.set_page_config(page_title="AI research agent", page_icon=":bird:")
    
    st.header("AI research agent :bird:")
    query = st.text_input("Research goal")
    
    if query:
        st.write("Doing research for ", query)
        
        result = agent({"input": query})
        
        st.info(result['output'])
        
        
        
if __name__ == '__main__':
    main()'''
    
    

# 5. Set this as an API endpoint via FastAPI
# https://fastapi.tiangolo.com/
# to turn this app into API endpoint easily
# TO RUN IT:
# uvicorn app:app --host 0.0.0.0 --port 10000
app = FastAPI()

class Query(BaseModel):
    query: str
    
@app.post("/")
def researchAgent(query: Query):
    query = query.query
    content = agent({"input": query})
    actual_content = content['output']
    return actual_content
    # return content            # to get all the actual elements e.g. memory