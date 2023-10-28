# TO RUN:
# chainlit run app.py

import os
import chainlit as cl
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings, OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

load_dotenv()

llm = OpenAI(temperature=0.1, openai_api_key=os.getenv("OPENAI_API_KEY"))

loader = DirectoryLoader("data/", glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)

memory = ConversationBufferMemory(memory_keys="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(
    llm = llm,
    memory = memory,
    chain_type = "stuff",
    retriever = vectorstore.as_retriever(search_kwargs={"k":2})
)

def on_chat_start(event):
    # Initialize the conversation buffer memory
    memory.reset()

def on_message(event):
    # Get the user's message
    message = event.message

    # Generate a response using the chain
    response = chain.generate(message=message, memory=memory)

    # Send the response back to the user
    event.send_message(response)

# Start the chainlit app
cl.run(on_chat_start=on_chat_start, on_message=on_message)