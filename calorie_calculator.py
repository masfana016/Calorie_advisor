from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

load_dotenv()

llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = PromptTemplate(
    template="You are a tool caller: You have to call the tool named add_numbers in case if any addition and subtraction requires. Please don't send any explanation while calling function, just send three numbers, gender, and activity level that the user provided in comma. e.g., 5, 2, 3, male, sedentary. If a condition exists in a function to check the gender and activity level, use the result according to that. Even if the user has sent a sentence, you have to find three numbers, gender, and activity level, then pass them to the function. User input is {input}\n",
    inputVariable=["input"]
)

@tool
def add_numbers(user_input: str) -> str:
    """Add two numbers and abstract the 3rd number based on gender and activity level."""
    print("User input:", user_input)
    try:
        # Split the input into parts
        data = user_input.split(",")
        # Check if we have exactly five parts (three numbers, gender, and activity level)
        if len(data) != 5:
            return "Invalid input. Please provide three numbers, gender, and activity level in the format: num1, num2, num3, gender, activity_level."
        
        # Extract numbers, gender, and activity level
        age, weight, height, gender, activity_level = (
            float(data[0]),
            float(data[1]),
            float(data[2]),
            data[3].strip().lower(),
            data[4].strip().lower(),
        )
        
        # Activity multipliers based on activity level
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly active": 1.375,
            "moderately active": 1.55,
            "very active": 1.725,
            "super active": 1.9,
        }
        
        # Validate activity level
        if activity_level not in activity_multipliers:
            return "Invalid activity level. Please choose from: sedentary, lightly active, moderately active, very active, or super active."
        
        # Calculate result based on gender
        if gender in ["male", "men"]:
            base_result = 88.362 + (13.397 * age) + (4.799 * weight) - (5.677 * height)
        elif gender in ["female", "women"]:
            base_result = 47.593 + (9.247 * age) + (3.098 * weight) - (4.330 * height)
        else:
            return "Gender must be either 'male' or 'female'."
        
        # Apply activity multiplier
        final_result = base_result * activity_multipliers[activity_level]
        return f"{final_result}"
    
    except (ValueError, IndexError) as e:
        return "No valid numbers found or insufficient input."

chain = RunnableSequence (
    prompt_template,
    llm,
    add_numbers,
)

response = chain.invoke("2, 3, 5, female, moderately active")
print("Output:", response)
