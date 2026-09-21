"""
Directs incoming messages to the correct flow based on intent
and current conversation state.
"""

from src.chat.conversation import get_or_create, set_classifying, set_idle
from src.chat.intent import classify_intent
from src.rag.retrieval.retriever import retrieve
from src.rag.generation.generator import generate
from src.agent.agent import run_agent


def handle_message(conversation_id: str, message: str) -> dict:
    """
    Handle an incoming chat message and return a response.

    Args:
        conversation_id: Unique identifier for the conversation.
        message: The user's message.

    Returns:
        A dict with "type" and relevant response fields.
    """
    state = get_or_create(conversation_id)

    intent = classify_intent(
        message=message,
        state=state.state,
        pending_question=state.pending_question
    )

    # If a classification is in progress but the user switches topic,
    # reset to IDLE before handling the new intent.
    if state.state == "CLASSIFYING" and intent != "risk_classification_followup":
        set_idle(conversation_id)

    if intent == "rag_query":
        chunks = retrieve(message)
        result = generate(message, chunks)
        return {
            "type": "rag_response",
            "answer": result["answer"],
            "sources": result["sources"]
        }

    if intent == "risk_classification":
        messages = [{"role": "user", "content": message}]
        result = run_agent(messages)

        if result["status"] == "follow_up":
            set_classifying(
                conversation_id=conversation_id,
                session_id=result.get("session_id", conversation_id),
                pending_question=result["question"],
                pending_tool_use_id=result["tool_use_id"],
                messages=result["messages"]
            )
            return {
                "type": "follow_up",
                "question": result["question"]
            }

        set_idle(conversation_id)
        if "report" not in result:
            return {
                "type": "rag_response",
                "answer": "Classification could not be completed. Please try again with more details about your AI system.",
                "sources": []
            }
        return {
            "type": "classification",
            "report": result["report"]
        }

    if intent == "risk_classification_followup":
        # Inject the user's answer as a proper tool_result for the pending tool_use.
        messages = state.messages
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": state.pending_tool_use_id,
                "content": message
            }]
        })

        result = run_agent(messages)

        if result["status"] == "follow_up":
            set_classifying(
                conversation_id=conversation_id,
                session_id=state.session_id,
                pending_question=result["question"],
                pending_tool_use_id=result["tool_use_id"],
                messages=result["messages"]
            )
            return {
                "type": "follow_up",
                "question": result["question"]
            }

        set_idle(conversation_id)
        if "report" not in result:
            return {
                "type": "rag_response",
                "answer": "Classification could not be completed. Please try again with more details about your AI system.",
                "sources": []
            }
        return {
            "type": "classification",
            "report": result["report"]
        }