import google.generativeai as genai
from config import APIKEY

genai.configure(api_key=APIKEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_test_cases(code: str, design: str, user_story: str):
    
    prompt = (
        f"You are a Senior QA Engineer. Based on the following technical design and implementation code:\n\n"
        f"Design:{design}"
        f"Code: {code}"
        f"user stories: {user_story}"
        f"Your tasks:"
        f"1. Generate at least 5 detailed unit test cases in points like 1, 2, 3... that validate key functionalities based on the design."
        f"2. Simulate the test cases against the provided code."
        f"3. Important: Report the test result summary in the format: 'X test cases passed, Y failed'."
        f"4. Ensure the test cases are clear, relevant, and cover both typical scenarios and edge cases where applicable."
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.8,
            "max_output_tokens": 1000  # Use this instead of max_tokens
        }
    )

    # Extract the output text
    test_cases = response.text if hasattr(response, 'text') else str(response)

    return test_cases
