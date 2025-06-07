from typing import Protocol


class LoggerProtocol(Protocol):
    def log(self, message: str) -> None:
        ...


class ConsoleLogger(LoggerProtocol):
    def log(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class FileLogger(LoggerProtocol):
    def __init__(self, filename: str = "log.txt") -> None:
        self.filename = filename

    def log(self, message: str) -> None:
        with open(self.filename, "a") as f:
            f.write(f"[FILE] {message}\n")


class DatabaseProtocol(Protocol):
    def query(self, sql: str) -> None:
        ...


class SqlDatabase(DatabaseProtocol):
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def query(self, sql: str) -> str:
        return f"Executed: {sql} on {self.connection_string}"


class MockDatabase(DatabaseProtocol):
    def query(self, sql: str) -> str:
        return f"Mocked: {sql}"


class EmailServiceProtocol(Protocol):
    def send(self, to: str, subject: str, body: str) -> None:
        ...


class SmtpEmailService(EmailServiceProtocol):
    def __init__(self, smtp_server: str) -> None:
        self.smtp_server = smtp_server

    def send(self, to: str, subject: str, body: str) -> str:
        return f"Sent via {self.smtp_server} to {to}: {subject}"


class MockEmailService(EmailServiceProtocol):
    def send(self, to: str, subject: str, body: str) -> str:
        return f"Mock email to {to}: {subject}"
