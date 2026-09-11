import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the AI model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load evidence
with open("evidence.json", "r", encoding="utf-8") as file:
    evidence_data = json.load(file)


# Create embeddings for all evidence
evidence_texts = [item["text"] for item in evidence_data]
evidence_embeddings = model.encode(evidence_texts)


def retrieve_evidence(claim, top_k=3):

    # Convert claim into embedding
    claim_embedding = model.encode([claim])

    # Compare claim with all evidence
    similarities = cosine_similarity(
        claim_embedding,
        evidence_embeddings
    )[0]

    # Add similarity score to each evidence item
    results = []

    for i, score in enumerate(similarities):
        results.append({
            "id": evidence_data[i]["id"],
            "text": evidence_data[i]["text"],
            "source": evidence_data[i]["source"],
            "similarity_score": round(float(score), 4)
        })

    # Sort from highest similarity to lowest
    results.sort(
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    # Return top results
    return results[:top_k]
