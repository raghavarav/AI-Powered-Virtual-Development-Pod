import google.generativeai as genai
from config import APIKEY

genai.configure(api_key=APIKEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")



async def manager_chat(user_story: str, design: str, code: str, test_cases: str, query: str, conversation_history):

    if not all([user_story, design, code, test_cases]):
        return "Let's get the project implemented first—then I'll be ready to answer your queries!"

    prompt = (
        f"You are a Senior Technical Assistant. Based on the following project context, respond accurately to the user's query.\n\n"
        f"User Story: {user_story}"
        f"Design:\n\"\"\"\n{design}\n\"\"\"\n\n"
        f"Code Implementation:\n\"\"\"\n{code}\n\"\"\"\n\n"
        f"Test Cases:\n\"\"\"\n{test_cases}\n\"\"\"\n\n"
        f"User Query:\n\"\"\"\n{query}\n\"\"\"\n\n"
        f"Your task:\n"
        f"1. Carefully analyze all the provided information.\n"
        f"2. Provide a clear, concise, and technically accurate response to the user's query.\n"
        f"3. If needed, reference relevant parts of the design, code, or test cases to support your answer.\n"
        f"4. Ensure the response is helpful, structured, and follows professional communication standards."
        f"conversational history: {conversation_history}"
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.8,
            "max_output_tokens": 1000  # Use this instead of max_tokens
        }
    )

    chat = response.text if hasattr(response, 'text') else str(response)
    conversation_history.append({"user_query": query, "response": chat})

    return chat
