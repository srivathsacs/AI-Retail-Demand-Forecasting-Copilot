from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

text = """
HIGH Stockout Risk

Projected inventory falls below safety stock.
Review inventory position.
Evaluate replenishment options.
"""

embedding = model.encode(text)

print(f"Vector Length: {len(embedding)}")
print()
print(embedding[:10])