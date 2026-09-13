from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL


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
        prompt_name="query",
        normalize_embeddings=True
    )

    return embedding.tolist()