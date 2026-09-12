from sentence_transformers import SentenceTransformer
import chromadb
from langchain_core.prompts import PromptTemplate
from google import genai
from dotenv import load_dotenv
import os


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to Chroma once
chroma_client = chromadb.PersistentClient(path="chroma_db")


# Load collection once
collection = chroma_client.get_collection(
    name="inventory_knowledge_base"
)


# Load environment variables once
load_dotenv()


# Create Gemini client once
gemini_client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def ask_question(question):
    """
    Input:
        question (str)

    Output:
        answer (str)
    """

    # Convert question to embedding
    query_embedding = model.encode(question).tolist()

    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    # Extract chunks
    retrieved_chunks = results["documents"][0]

    # Create context
    context = "\n\n".join(retrieved_chunks)

    # Prompt template
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

    # Build final prompt
    final_prompt = prompt_template.format(
        context=context,
        question=question
    )

    # Gemini call
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    return response.text


if __name__ == "__main__":
    question = "What should I do for critical stockout risk?"

    answer = ask_question(question)

    print(answer)