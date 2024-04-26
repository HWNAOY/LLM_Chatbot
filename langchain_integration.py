import chainlit as cl
import openai
import os
from langchain_core.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from langchain.chains.llm import LLMChain

os.environ['OPENAI_API_KEY'] = ""

template = """Question: {question}

Answer: Let's think step by step."""

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template = template, input_variables = ["question"])
    llm_chain = LLMChain(
        prompt = prompt,
        llm = OpenAI(temperature = 1, streaming = True, openai_api_key=os.environ.get("OPENAI_API_KEY")),
        verbose = True
    )

    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message : str):
    llm_chain = cl.user_session.get("llm_chain")
    res = await llm_chain.acall(message, callbacks = [cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content = res["text"]).send()