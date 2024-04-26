from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
import os
import chainlit as cl

#pip install arxiv

llm = ChatOpenAI(temperature = 0.3)
tools = load_tools(
    ["arxiv"]
)

agent_chain = initialize_agent(
    tools,
    llm,
    max_interactions = 5,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)
cl.user_session.set("agent", agent_chain)

agent_chain.run(
    "what is RLHF?",
)

@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message, callbacks=[cb])
