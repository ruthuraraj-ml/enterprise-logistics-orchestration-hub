from datetime import datetime
import threading

class EventLogger:
    def __init__(self):
        self.events = []
        self._lock = threading.Lock()
        
    def clear(self):
        with self._lock:
            self.events = []

    def log(self, message: str):
        """Appends a timestamped log line safely across threads."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with self._lock:
            self.events.append(f"[{timestamp}] ⚙️ {message}")

    def get_events(self) -> str:
        """Returns the full log stream as a newline-separated block."""
        with self._lock:
            return "\n".join(self.events)