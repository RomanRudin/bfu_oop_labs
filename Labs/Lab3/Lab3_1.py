from abc import ABC, abstractmethod
from typing import Protocol
import socket
import re
from datetime import datetime

class LogFilterProtocol(Protocol):
    @abstractmethod
    def match(self, message: str) -> bool:
        pass

class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, message: str) -> bool:
        return self.pattern in message
    
class ReLogFilter(LogFilterProtocol):
    def __init__(self, regex_pattern: str):
        self.regex = re.compile(regex_pattern)

    def match(self, message: str) -> bool:
        return bool(self.regex.search(message))

class LogHandlerProtocol(Protocol):
    @abstractmethod
    def handle(self, message: str) -> None:
        pass

class FileHandler(LogHandlerProtocol):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def handle(self, message: str) -> None:
        with open(self.filepath, 'a') as file:
            file.write(f'{datetime.now().isoformat()} {message}\n')

class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int, protocol: str = 'tcp'):
        self.host = host
        self.port = port
        self.protocol = protocol.lower()

    def handle(self, message: str) -> None:
        try:
            if self.protocol == 'udp':
                self._send_udp(message)
            else:
                self._send_tcp(message)
        except Exception as e:
            print(f'Socket error: {e}')

    def _send_tcp(self, message: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(f'{message}\n'.encode('utf-8'))

    def _send_udp(self, message: str):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(f'{message}\n'.encode('utf-8'), (self.host, self.port))

class ConsoleHandler(LogHandlerProtocol):
    def handle(self, message: str) -> None:
        print(f'[CONSOLE] {datetime.now().isoformat()} {message}')

class SysLogHandler(LogHandlerProtocol):
    def __init__(self, host: str = 'localhost', port: int = 514, 
                 facility: int = 1, severity: int = 6):
        self.host = host
        self.port = port
        self.priority = facility * 8 + severity

    def handle(self, message: str) -> None:
        try:
            timestamp = datetime.now().strftime('%b %d %H:%M:%S')
            hostname = socket.gethostname()
            syslog_msg = (
                f'<{self.priority}>1 '
                f'{timestamp} {hostname} '
                f'PythonLogger - - {message}'
            )
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(syslog_msg.encode('utf-8'), (self.host, self.port))
        except Exception as e:
            print(f'Syslog error: {e}')

class Logger:
    def __init__(self, handlers: list[LogHandlerProtocol], 
                 filters: list[LogFilterProtocol], settings_file=None):
        self.handlers = handlers
        self.filters = filters

    def write(self, message: str) -> None:
        if any(f.match(message) for f in self.filters):
            for handler in self.handlers:
                handler.handle(message)

# Тестовые примеры
if __name__ == '__main__':
    # Инициализация обработчиков
    handlers = [
        ConsoleHandler(),
        FileHandler('app.log'),
        SocketHandler('localhost', 5140, 'udp'),
        SysLogHandler(port=5514)
    ]

    # Инициализация фильтров
    filters = [
        SimpleLogFilter('IMPORTANT'),
        ReLogFilter(r'(ERROR|WARNING) \d+')
    ]

    # Создание логгера
    logger = Logger(handlers, filters, None)

    # Тестовые сообщения
    test_messages = [
        'INFO: System started',
        'IMPORTANT: Critical update required',
        'ERROR 404: Resource not found',
        'WARNING 101: High temperature',
        'DEBUG: Connection established'
    ]

    for msg in test_messages:
        logger.write(msg)