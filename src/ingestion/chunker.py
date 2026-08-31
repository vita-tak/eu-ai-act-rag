import re

def chunk_document(text: str) -> list:
    # Split the text into chunks based on headings (e.g., "Article 1", "Article 2", etc.)
    chunks = re.split(r'(^Article \d+$)', text, flags=re.MULTILINE)
    
    # Combine the heading with its corresponding content
    combined_chunks = []
    for i in range(1, len(chunks), 2):
        heading = chunks[i]
        content = chunks[i + 1] if i + 1 < len(chunks) else ""
        combined_chunks.append({"article": heading.strip(), "text": content.strip()})
    return combined_chunks