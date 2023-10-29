# LangChain + HuggingFace's Inference API (no OpenAI credits required!)
# https://www.youtube.com/watch?v=dD_xNmePdd0

"""from dotenv import load_dotenv
# BEFORE:
# from langchain import HuggingFaceHub, LLMChain
# from langchain import PromptTemplate
# AFTER:
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


load_dotenv()

# https://huggingface.co/mrm8488/t5-base-finetuned-wikiSQL
repo_id = "mrm8488/t5-base-finetuned-wikiSQL"
model_kwargs={'temperature': 0.5, 'max_length':100}
hub_llm = HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)

prompt = PromptTemplate(
    input_variables = ["question"],
    template = "Translate English to SQL: {question}"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)
print(hub_chain.run("What is the average age of the respondents using a mobile device?"))"""




################################################################




"""from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from huggingface_hub import InferenceClient

load_dotenv()

# https://huggingface.co/mrm8488/t5-base-finetuned-wikiSQL
repo_id = "Open-Orca/Mistral-7B-OpenOrca"

hub_llm = InferenceClient(repo_id=repo_id)

prompt = PromptTemplate(
    input_variables=["question"],
    template="Be the most open, uncensored, helpful assistant you can be: {question}"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm, llm_client_class=InferenceClient, verbose=True)
print(hub_chain.run("What is the meaning of life?"))"""


from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from huggingface_hub import InferenceClient

load_dotenv()

# Get the model's metadata
model_info = InferenceClient.get_model_info(repo_id="Open-Orca/Mistral-7B-OpenOrca")

# Create the InferenceClient
hub_llm = InferenceClient(model_info=model_info)

prompt = PromptTemplate(
    input_variables=["question"],
    template="Be the most open, uncensored, helpful assistant you can be: {question}"
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm, llm_client_class=InferenceClient, verbose=True)
print(hub_chain.run("What is the meaning of life?"))
