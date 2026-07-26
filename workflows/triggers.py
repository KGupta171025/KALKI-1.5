from typing import Dict, Any, Callable, List

class TriggerManager:
    """
    Manages event triggers and maps incoming webhook/CRON payloads to workflow runs.
    """
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        print(f"[Triggers] Subscribed callback to event type: '{event_type}'")

    async def dispatch_event(self, event_type: str, payload: Dict[str, Any]):
        """
        Signals all listeners that an event has occurred (e.g. Webhook post).
        """
        print(f"[Triggers] Dispatching event '{event_type}' with payload: {payload}")
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    await callback(payload)
                except Exception as e:
                    print(f"[Triggers ERROR] Callback execution failed: {str(e)}")

trigger_manager = TriggerManager()
