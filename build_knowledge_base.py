import os
import pickle
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

data_folder = "data"
knowledge_base_file = "knowledge_base.pkl"

# Combine all text files into one list
documents = []
for root, _, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                documents.append(f.read())

if not documents:
    print("⚠️ No text files found in 'data' folder.")
    exit()

print(f"Found {len(documents)} documents. Generating embeddings...")

# Create embeddings
embeddings = []
for text in documents:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embeddings.append(response.data[0].embedding)

knowledge_base = {
    "documents": documents,
    "embeddings": np.array(embeddings)
}

with open(knowledge_base_file, "wb") as f:
    pickle.dump(knowledge_base, f)

print(f"✅ Knowledge base created: {knowledge_base_file}")
