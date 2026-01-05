class SessionState:
    """
    Lightweight per-session memory.
    """
    def __init__(self):
        self.chat_history = []
        self.pending_task = None


state = SessionState()
