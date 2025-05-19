from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None: pass

class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[CONSOLE] {message}")

class FileLogger(ILogger):
    def __init__(self, filename: str = "log.txt") -> None:
        self.filename = filename
    
    def log(self, message: str) -> None:
        with open(self.filename, "a") as f:
            f.write(f"[FILE] {message}\n")

class IDatabase(ABC):
    @abstractmethod
    def query(self, sql: str) -> None: pass

class SqlDatabase(IDatabase):
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
    
    def query(self, sql: str) -> str:
        return f"Executed: {sql} on {self.connection_string}"

class MockDatabase(IDatabase):
    def query(self, sql: str) -> str:
        return f"Mocked: {sql}"

class IEmailService(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: pass

class SmtpEmailService(IEmailService):
    def __init__(self, smtp_server: str) -> None:
        self.smtp_server = smtp_server
    
    def send(self, to: str, subject: str, body: str) -> str:
        return f"Sent via {self.smtp_server} to {to}: {subject}"

class MockEmailService(IEmailService):
    def send(self, to: str, subject: str, body: str) -> str:
        return f"Mock email to {to}: {subject}"
