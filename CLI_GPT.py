from langchain_community.tools import ShellTool
from langchain_openai import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import os

shell_tool = ShellTool()

llm = ChatOpenAI(temperature = 0)

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")
agent = initialize_agent(
    [shell_tool], llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose = True
)

agent.run(
    "Create a text file called empty and inside it, add code that trains a convolutional neural network for 3 epochs"
)
