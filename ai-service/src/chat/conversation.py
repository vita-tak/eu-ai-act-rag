"""
Conversation state management for the chat endpoint.

Tracks the state of each conversation (IDLE or CLASSIFYING) and
the associated classification session when one is in progress.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConversationState:
    state: str = "IDLE"
    session_id: Optional[str] = None
    pending_question: Optional[str] = None
    pending_tool_use_id: Optional[str] = None
    messages: list = field(default_factory=list)


conversations: dict[str, ConversationState] = {}


def get_or_create(conversation_id: str) -> ConversationState:
    """Get existing conversation state or create a new one."""
    if conversation_id not in conversations:
        conversations[conversation_id] = ConversationState()
    return conversations[conversation_id]


def set_classifying(conversation_id: str, session_id: str, pending_question: str, pending_tool_use_id: str, messages: list) -> None:
    """Transition conversation to CLASSIFYING state."""
    state = get_or_create(conversation_id)
    state.state = "CLASSIFYING"
    state.session_id = session_id
    state.pending_question = pending_question
    state.pending_tool_use_id = pending_tool_use_id
    state.messages = messages


def set_idle(conversation_id: str) -> None:
    """Transition conversation back to IDLE, clearing classification state."""
    state = get_or_create(conversation_id)
    state.state = "IDLE"
    state.session_id = None
    state.pending_question = None
    state.pending_tool_use_id = None
    state.messages = []