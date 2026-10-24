"""
agentP - Event-Driven Pub-Sub Bus (Sprint 7)
Pattern: Event Bus / Observer Pattern
Author: Carlos (Backend Dev) & Liam (DevOps)
Provides pub-sub messaging, streaming events, and channel subscriptions between agents and client UI.
"""

import time
import json
import threading
from typing import Dict, Any, List, Callable, Optional

class EventPubSubBus:
    """Thread-safe event bus for real-time agent communications, summoning, and UI updates."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventPubSubBus, cls).__new__(cls)
                cls._instance._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
                cls._instance._event_history: List[Dict[str, Any]] = []
                cls._instance._seq = 0
            return cls._instance

    @classmethod
    def reset(cls):
        """Resets the singleton for clean testing."""
        inst = cls()
        inst._subscribers.clear()
        inst._event_history.clear()
        inst._seq = 0

    def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribes a listener to a specific event channel."""
        if channel not in self._subscribers:
            self._subscribers[channel] = []
        self._subscribers[channel].append(callback)

    def unsubscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]):
        """Unsubscribes a listener."""
        if channel in self._subscribers and callback in self._subscribers[channel]:
            self._subscribers[channel].remove(callback)

    def publish(self, channel: str, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Publishes an event to a channel and returns the envelope."""
        with self._lock:
            self._seq += 1
            envelope = {
                "seq": self._seq,
                "channel": channel,
                "type": event_type,
                "data": data,
                "timestamp": time.time(),
                "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self._event_history.append(envelope)
            # Keep history under 500 events
            if len(self._event_history) > 500:
                self._event_history.pop(0)

        # Dispatch to subscribers
        listeners = self._subscribers.get(channel, []) + self._subscribers.get("*", [])
        for cb in listeners:
            try:
                cb(envelope)
            except Exception as e:
                print(f"[PubSub] Error invoking listener: {e}")

        return envelope

    def get_history(self, channel: Optional[str] = None, since_seq: int = 0) -> List[Dict[str, Any]]:
        """Retrieves past events for client sync or replay."""
        with self._lock:
            events = [e for e in self._event_history if e["seq"] > since_seq]
            if channel:
                events = [e for e in events if e["channel"] == channel]
            return list(events)
