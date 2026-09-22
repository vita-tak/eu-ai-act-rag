"""
Intent classification for the chat endpoint.

Classifies incoming messages into one of three intents based on
the message content and current conversation state:
- rag_query: question about the EU AI Act
- risk_classification: request to classify an AI system's risk level
- risk_classification_followup: answer to a pending follow-up question
"""

import json
import anthropic
from src.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

INTENTS = ["rag_query", "risk_classification", "risk_classification_followup"]


def classify_intent(message: str, state: str, pending_question: str = None) -> str:
    """
    Classify the user's message into one of three intents.

    Args:
        message: The user's message.
        state: Current conversation state, either "IDLE" or "CLASSIFYING".
        pending_question: The follow-up question the agent is waiting on,
                          only present when state is "CLASSIFYING".

    Returns:
        One of: "rag_query", "risk_classification", "risk_classification_followup".
    """
    context = ""
    if state == "CLASSIFYING" and pending_question:
        context = f"\nThe assistant is currently waiting for an answer to: '{pending_question}'"

    system_prompt = f"""You are an intent classifier for an EU AI Act assistant.

Current conversation state: {state}{context}

Classify the user's message into exactly one of these intents:
- rag_query: the user is asking a question about the EU AI Act, its articles,
  requirements, definitions, or how it works. This includes questions about
  the classification process itself, such as "How do I classify my AI system?"
  or "What risk category am I in?" without providing a system description.
  These are questions about the process, not classification requests.
- risk_classification: the user is describing an AI system they own or are building
  and wants to know its risk level under the EU AI Act
- risk_classification_followup: the user is answering a follow-up question in an
  ongoing risk classification

Key distinction: if the user describes "my system", "our system", "an AI system that does X",
or asks "what risk category does X fall under" while describing a specific system,
classify as risk_classification.
If the user asks "what does Article X say", "how does the EU AI Act define X",
or asks about the classification process without describing a specific system,
classify as rag_query.

If the state is CLASSIFYING and the message looks like a direct answer to the pending question,
classify it as risk_classification_followup.
If the state is CLASSIFYING but the message is clearly a new question or a new topic,
classify it as rag_query or risk_classification instead.

Respond with JSON only, no other text:
{{"intent": "rag_query"}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {"role": "user", "content": message}
        ],
        system=system_prompt
    )

    raw = response.content[0].text.strip()
    # Strip markdown code blocks if present.
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        result = json.loads(raw)
        intent = result.get("intent")
    except json.JSONDecodeError:
        return "rag_query"

    # Fall back to rag_query if the response is unexpected.
    if intent not in INTENTS:
        return "rag_query"

    return intent