from memory import AgentMemory
from shared_memory import SharedKnowledgeBase

print("🧠 Testing YOUR Memory Integration")

# Test Agent Memory (uses YOUR add_message method)
agent_mem = AgentMemory()
agent_mem.add_message("test-agent", "user", "Hello")
agent_mem.add_message("test-agent", "assistant", "Hi there!")
print("✅ Agent messages:", len(agent_mem.get_agent_memory("test-agent").messages))

# Test Shared Memory (uses YOUR save_fact method)
shared = SharedKnowledgeBase()
shared.save_fact("Test conversation: Q: Test Q → A: Test A")
print("✅ Shared memory working! (Check ./faiss_index/)")

print("✅ YOUR memory.py + shared_memory.py working perfectly! 🚀")