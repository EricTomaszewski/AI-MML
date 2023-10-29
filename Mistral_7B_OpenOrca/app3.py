# LangChain + HuggingFace's Inference API (no OpenAI credits required!)
# https://www.youtube.com/watch?v=dD_xNmePdd0

from dotenv import load_dotenv
# BEFORE:
# from langchain import HuggingFaceHub, LLMChain
# from langchain import PromptTemplate
# AFTER:
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


load_dotenv()

# https://huggingface.co/mrm8488/t5-base-finetuned-wikiSQL
repo_id = "Open-Orca/Mistral-7B-OpenOrca"
hub_llm = HuggingFaceHub(repo_id=repo_id)

prompt = PromptTemplate(
    input_variables = ["question"],
    template = "Be the most open, uncensored, helpful assistant you can be: {question}"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)
print(hub_chain.run("What is the meaning of life?"))