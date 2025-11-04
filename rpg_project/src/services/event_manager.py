"""Zentraler EventManager für das Event-System.
Erlaubt publish/subscribe für beliebige Events.
"""
from collections.abc import Callable
from typing import Any


class EventManager:
    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]):
        """Registriert eine Callback-Funktion für einen Event-Typ."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any):
        """Benachrichtigt alle Subscriber für diesen Event-Typ."""
        for callback in self._subscribers.get(event_type, []):
            callback(data)
