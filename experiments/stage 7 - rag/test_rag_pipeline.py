from sentence_transformers import SentenceTransformer
import chromadb
from langchain_core.prompts import PromptTemplate


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to Chroma
client = chromadb.PersistentClient(path="chroma_db")


# Load collection
collection = client.get_collection(
    name="inventory_knowledge_base"
)


# User question
question = "What should I do for critical stockout risk?"


# Convert question to embedding
query_embedding = model.encode(question).tolist()


# Retrieve top 3 chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)


print(results["documents"][0])


# Extract retrieved chunks
retrieved_chunks = results["documents"][0]


# Combine chunks into one context string
context = "\n\n".join(retrieved_chunks)


# Create prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an inventory policy assistant.

Context:
{context}

Question:
{question}
"""
)


# Fill template with actual values
final_prompt = prompt_template.format(
    context=context,
    question=question
)


# Print final prompt
#print(final_prompt)


from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt
)

print(response.text)