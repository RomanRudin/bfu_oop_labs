class OutputState:
    def __init__(self) -> None:
        self.text = ""
        self.volume = 50
        self.media_playing = False
        
    def add_char(self, char: str) -> None:
        self.text += char
        
    def remove_char(self) -> None:
        if self.text:
            self.text = self.text[:-1]
            
    def get_state(self) -> dict[str, str | int | bool]:
        return {
            "text": self.text,
            "volume": self.volume,
            "media_playing": self.media_playing
        }
        
    def set_state(self, state: dict) -> None:
        self.text = state.get("text", "")
        self.volume = state.get("volume", 50)
        self.media_playing = state.get("media_playing", False)
