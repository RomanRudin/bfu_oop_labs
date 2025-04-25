from protocols import PropertyChangedListenerProtocol, DataChangedProtocol, COLORING

class ConsoleLogger(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj: DataChangedProtocol, property_name: str) -> None:
        print(COLORING.format(32, f"[LOG] Property {property_name} changed in {str(obj)}"))