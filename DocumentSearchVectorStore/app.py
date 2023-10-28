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

@cl.langchain_factory(use_async=False)
def factory():
    chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        memory = memory,
        chain_type = "stuff",
        retriever = vectorstore.as_retriever(search_kwargs={"k":2})
    )
    return chain



def main():
    # Instantiate the chain for that user session
    prompt = ConversationalRetrievalChain.from_llm(
        llm = llm,
        memory = memory,
        chain_type = "stuff",
        retriever = vectorstore.as_retriever(search_kwargs={"k":2})
    )
    
    # llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)
    

    # Store the chain in the user session
    cl.user_session.set("llm_chain", prompt)
    
    
@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here

    # Send the response
    await cl.Message(content=res["text"]).send()




'''@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here

    # Send the response
    await cl.Message(content=res["text"]).send()'''