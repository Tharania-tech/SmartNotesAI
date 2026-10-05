from services.text_chunk_service import (
    TextChunkService
)


text = """
HTML is used to create web pages.
CSS controls the appearance of web pages.
JavaScript provides interactivity.
XML represents structured data.
JSP is used to create dynamic web pages.
Servlets process HTTP requests.
MVC separates an application into Model,
View, and Controller.
""" * 100


chunks = TextChunkService.chunk_text(
    text,
    max_words=50,
    overlap_words=10
)


print(
    f"\nTotal chunks: {len(chunks)}\n"
)

for index, chunk in enumerate(
    chunks,
    start=1
):

    print(
        f"========== CHUNK {index} =========="
    )

    print(
        chunk[:500]
    )

    print()