from app.models.agent import Agent
from app.models.chat import ChatMessage
from app.models.chat import ChatSession

TABLES = ["Agent", "ChatSession", "ChatMessage"]
ASSOCIATIONS = []

__all__ = TABLES + ASSOCIATIONS
