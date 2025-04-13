#Generate Vector DB file and Chunks and Save it Using This Code
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# === 1. Load text from file ===
with open("text_file_path.txt", "r", encoding="utf-8") as file:
    large_text = file.read()

# === 2. Chunk the text ===
def chunk_text(text, chunk_size=200):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = chunk_text(large_text)

# === 3. Generate embeddings ===
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# === 4. Create FAISS index ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# === 5. Save index and chunks ===
faiss.write_index(index, "my_index.faiss")

with open("my_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ Index and chunks saved successfully.")
