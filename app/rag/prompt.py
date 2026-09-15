def build_prompt(context, question):

    prompt = f"""
You are a document analysis assistant.

Answer the user's question using only the information
provided in the document context, in detail

Use the source and page information when relevant.

If the answer cannot be supported by the context,
say that the information was not found in the uploaded documents.

If the question is irrelevant to the context provided, 
and can be answered with your given knowledge base,
do answer it.

Do not invent facts.

Document context:
{context}

Question:
{question}

Answer:
"""

    return prompt