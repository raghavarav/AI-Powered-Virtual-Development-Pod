import google.generativeai as genai
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from config import APIKEY

genai.configure(api_key=APIKEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_code(design: str):
    index = faiss.read_index("vector_db_index_chunks/code_vector_db_index.faiss") #Load Vector DB

    with open("vector_db_index_chunks/code_chunks.pkl", "rb") as f: #Load Chunks
        chunks = pickle.load(f)
    
    embeder = SentenceTransformer("all-MiniLM-L6-v2") #Embedding Model

    query_embedding = embeder.encode([design]) #encodeing User Input
    distances, indices = index.search(np.array(query_embedding), k=3) #Semantic Searching

    matched_chunks = [chunks[i] for i in indices[0]] #Relevant Chunks in List

    
    prompt = (
        f"You are an experienced Software Developer. Based on the following technical design:"
        f"design: {design}"
        f"Generate simple, clean, efficient, and optimized HTML, CSS Javascript for frontend and use fastAPI OR Nodejs for backend code."
        f"Include comments where necessary to explain code logic."
        f"If applicable, structure the code into functions or classes."
        f"If possible, provide Folder structure"
        f"context: {matched_chunks}"
    )


    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.8,
            "max_output_tokens": 10000  # Use this instead of max_tokens
        }
    )

    # Extract the output text
    code = response.text if hasattr(response, 'text') else str(response)

    return code
