from langchain.tools import BaseTool

class CalorieCalculatorTool(BaseTool):
    # Adding type annotations for fields
    name: str = "calorie_calculator"
    description: str = "Calculates the calories needed based on user input (age, weight, height, gender, activity level)."

    def _run(self, user_input: str) -> str:
        # Parse user input
        user_data = self.parse_user_input(user_input)
        if not user_data:
            return "Please provide age, weight (kg), height (cm), gender (male/female), and activity level."

        age, weight, height, gender, activity_level = user_data

        # Perform BMR calculation
        bmr = self.calculate_bmr(age, weight, height, gender)

        # Calculate TDEE based on activity level
        tdee = self.calculate_tdee(bmr, activity_level)
        
        return f"Based on the input, your estimated daily calorie requirement is: {tdee:.2f} calories."

    def parse_user_input(self, user_input: str):
        try:
            data = user_input.split(',')
            age = int(data[0].strip())
            weight = float(data[1].strip())
            height = float(data[2].strip())
            gender = data[3].strip().lower()
            activity_level = data[4].strip().lower()
            return age, weight, height, gender, activity_level
        except (IndexError, ValueError):
            return None

    def calculate_bmr(self, age, weight, height, gender):
        if gender == "male":
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "female":
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            return 0  # Return 0 if gender is not male or female

    def calculate_tdee(self, bmr, activity_level):
        activity_factors = {
            "sedentary": 1.2,
            "lightly active": 1.375,
            "moderately active": 1.55,
            "very active": 1.725,
            "super active": 1.9
        }
        return bmr * activity_factors.get(activity_level, 1.2)  # Default to sedentary if invalid input
