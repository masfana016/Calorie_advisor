from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate (template ="Create a story about two friends who are going to market to buy some fruits. Use these character names {characters}, your response should be start from character name after the name add the colon e.g., name: , response should be json based", inputVariable = ["characters"] )

chain =  prompt | llm

response = chain.invoke({"characters": "Masfa and Musab"})

print (response)
