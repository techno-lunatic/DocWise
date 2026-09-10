# Generates embeddings 

from sentence_transformers import SentenceTransformer
# loads and runs embedding models

from app.config import EMBEDDING_MODEL
# the actual trained embedding model


model = SentenceTransformer(EMBEDDING_MODEL)


def embed_documents(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


def embed_query(query):

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()