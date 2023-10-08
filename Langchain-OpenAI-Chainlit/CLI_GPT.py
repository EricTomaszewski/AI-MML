from langchain.tools import ShellTool

shell_tool = ShellTool()

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import os


# os.environ['OPENAI_API_KEY'] = ''
# openai.api_key = '' 


llm = ChatOpenAI(temperature=0)

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")
agent = initialize_agent(
    [shell_tool], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, 
    handle_parsing_errors=True
)

agent.run(
    "create a text file called empty.txt and inside it, add code that trains a basic convolutional neural network for 4 epochs"
)

