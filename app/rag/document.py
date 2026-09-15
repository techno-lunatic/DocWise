# Generates a unique content-based ID for each PDF using SHA-256, (useful in chunking)
# which is used to uniquely identify the document and its chunks in ChromaDB.

# This is an optional part and can be skipped
# Creates a content-based ID,
# so the same document can always be uniquely identified, regardless of its filename or upload order.

import hashlib

def get_document_id(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(1024 * 1024)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()[:16]