
from typing import Protocol, Any

COLORING = "\033[{}m{}\033[0m"

class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        ...


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        ...
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        ...


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj: Any, property_name: str, 
                            old_value: Any, new_value: Any) -> bool:
        ...


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        ...
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        ...
