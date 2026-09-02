import anthropic
from src.config import ANTHROPIC_API_KEY, ANTHROPIC_WORKSPACE_ID


def generate(query: str, chunks: list) -> dict:
    """Build a prompt from query and chunks, call Claude, return answer and sources."""
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
        default_headers={"anthropic-workspace-id": ANTHROPIC_WORKSPACE_ID}
    )

    context = "\n\n".join([f"{chunk['article']}:\n{chunk['text']}" for chunk in chunks])

    prompt = f"""Here are relevant sections from the EU AI Act:

{context}

Based on these sections, answer the following question:
{query}

Always refer to the specific articles you are drawing from in your answer."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    sources = [chunk["article"] for chunk in chunks]

    return {
        "answer": message.content[0].text,
        "sources": sources
    }