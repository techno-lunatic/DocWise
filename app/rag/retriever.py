from app.rag.embeddings import embed_query
from app.rag.vector_store import get_collection

from app.config import TOP_K


def retrieve(query):

    query_vector = embed_query(query)

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=TOP_K
    )

    return results