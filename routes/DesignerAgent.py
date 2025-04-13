import google.generativeai as genai
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from config import APIKEY

genai.configure(api_key=APIKEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_design(user_story: str):
    index = faiss.read_index("vector_db_index_chunks/design_vector_db_index.faiss") #Load Vector DB

    with open("vector_db_index_chunks/design_chunks.pkl", "rb") as f: #Load Chunks
        chunks = pickle.load(f)
    
    embeder = SentenceTransformer("all-MiniLM-L6-v2") #Embedding Model

    query_embedding = embeder.encode([user_story]) #encodeing User Input
    distances, indices = index.search(np.array(query_embedding), k=3) #Semantic Searching

    matched_chunks = [chunks[i] for i in indices[0]] #Relevant Chunks in List


    prompt = (
        f"You are a Senior Software Architect. Based on the following user story:"
        f"user stories: {user_story}"
        f"Generate a detailed technical design including:"
        f"System architecture (components and interactions)"
        f"Database schema (entities, attributes, and relationships)"
        f"API design (endpoints, methods, request/response formats)"
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
    design = response.text if hasattr(response, 'text') else str(response)

    return design
