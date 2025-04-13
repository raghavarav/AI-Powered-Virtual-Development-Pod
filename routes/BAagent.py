import google.generativeai as genai
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from config import APIKEY

genai.configure(api_key=APIKEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_user_stories(user_input: str):
    index = faiss.read_index("vector_db_index_chunks/user_story_vector_db_index.faiss") #Load Vector DB

    with open("vector_db_index_chunks/user_story_chunks.pkl", "rb") as f: #Load Chunks
        chunks = pickle.load(f)
    
    embeder = SentenceTransformer("all-MiniLM-L6-v2") #Embedding Model

    query_embedding = embeder.encode([user_input]) #encodeing User Input
    distances, indices = index.search(np.array(query_embedding), k=3) #Semantic Searching

    matched_chunks = [chunks[i] for i in indices[0]] #Relevant Chunks in List

    prompt = (
        f"You are an Agile Business Analyst. "
        f"Based on the following input: {user_input}, generate a well-structured user story "
        f"in the standard industry-level Agile format: "
        f"As a [type of user], I want to [perform some action] so that [achieve some goal or benefit]."
        f"User Stories should be in points like 1, 2, 3..... and generate 5 or more user stories"
        f"context: {matched_chunks}"
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.8,
            "max_output_tokens": 1000  # Use this instead of max_tokens
        }
    )

    # Extract the output text
    user_stories = response.text if hasattr(response, 'text') else str(response)

    return user_stories
