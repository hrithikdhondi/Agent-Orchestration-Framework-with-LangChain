from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict

class AgentMemory:
    def __init__(self):
        self.agent_memories: Dict[str, ChatMessageHistory] = {}
    
    def get_agent_memory(self, agent_id: str) -> ChatMessageHistory:
        """Get conversation history for specific agent"""
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = ChatMessageHistory()
        return self.agent_memories[agent_id]
    
    def add_message(self, agent_id: str, role: str, content: str):
        """Add message to agent's memory"""
        history = self.get_agent_memory(agent_id)
        if role.lower() == "user":
            history.add_user_message(content)
        elif role.lower() == "assistant":
            history.add_ai_message(content)
        else:
            history.add_message({"role": role, "content": content})
    
    def get_context(self, agent_id: str, max_messages: int = 10) -> list:
        """Get recent conversation context for agent"""
        history = self.get_agent_memory(agent_id)
        return history.messages[-max_messages:] if len(history.messages) > max_messages else history.messages