# app/knowledge_base.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables from .env
load_dotenv()

# Read API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Knowledge base storage
chunks = []          # List of text chunks (FAQ or website content)
embeddings = None    # List of embeddings for each chunk

def build_index(faq_texts):
    """
    faq_texts: list of paragraphs / FAQ entries from website
    """
    global chunks, embeddings
    chunks = faq_texts
    embeddings = [client.embeddings.create(input=chunk, model="text-embedding-3-small")['data'][0]['embedding']
                  for chunk in chunks]

def query_knowledge_base(user_query, k=3):
    """
    Returns the most relevant answer from the knowledge base.
    Uses cosine similarity instead of FAISS.
    """
    if not chunks or not embeddings:
        return "Sorry, the knowledge base is not ready yet."

    query_emb = client.embeddings.create(input=user_query, model="text-embedding-3-small")['data'][0]['embedding']
    
    sims = cosine_similarity([query_emb], embeddings)[0]      # Compute similarity
    top_indices = sims.argsort()[-k:][::-1]                  # Top k similar chunks
    relevant_texts = "\n".join([chunks[i] for i in top_indices])
    
    # Generate answer using GPT
    prompt = f"Answer the question based on the following content:\n{relevant_texts}\n\nQuestion: {user_query}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
