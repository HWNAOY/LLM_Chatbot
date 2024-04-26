from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType, AgentExecutor
import os
import chainlit as cl

#pip install arxiv
os.environ['OPENAI_API_KEY'] = ""

@cl.on_chat_start
def start():
    llm = OpenAI(temperature = 0.5, streaming = True, openai_api_key=os.environ.get("OPENAI_API_KEY"))
    tools = load_tools(
        ["arxiv"]
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        max_interactions = 10,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    cl.user_session.set("agent", agent_chain)

# agent_chain.run(
#     "what is RLHF?",
# )

@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent") # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message, callbacks=[cb])
