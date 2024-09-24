import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langserve import add_routes
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

model = ChatGroq(model="Llama-3.1-8b-Instant")
parser = StrOutputParser()
prompt = ChatPromptTemplate([
    ("system","You are a language Translate. Translate the given input in {language}"),
    ("user","{input}")
])
chain = prompt|model|parser

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="It is a Language Translator"
)

add_routes(
    app,
    chain,
    path="/tapi"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)

# Use /docs to see documetation of all the api