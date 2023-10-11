from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Create a PromptTemplate object
prompt_template = PromptTemplate(
    input_template="Given {}, generate a response:",
    output_template="Response: {}",
)

# Create an LLMChain object
llm_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    prompt=prompt_template,
)

# Generate a response to a prompt
prompt = "Given that the weather is sunny, what should I wear today?"
response = llm_chain.generate(prompt)

print(response)