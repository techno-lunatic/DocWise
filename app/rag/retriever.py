from app.rag.embeddings import embed_query
from app.rag.vector_store import get_collection
from app.config import TOP_K


def retrieve(query):
    # Convert the user's question into an embedding vector
    query_vector = embed_query(query)

    # Get our ChromaDB collection
    collection = get_collection()

    # Search for the most similar document chunks
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=TOP_K
    )

    return results