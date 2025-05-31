from abc import ABC, abstractmethod
from typing import Protocol
import socket, re
from datetime import datetime



class LogFilterProtocol(Protocol):
    def match(self, message: str) -> bool:
        ...


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, message: str) -> bool:
        return self.pattern in message
    

class ReLogFilter(LogFilterProtocol):
    def __init__(self, regex_pattern: str) -> None:
        self.regex = re.compile(regex_pattern)

    def match(self, message: str) -> bool:
        return bool(self.regex.search(message))




class LogHandlerProtocol(Protocol):
    def handle(self, message: str) -> None:
        ...


class FileHandler(LogHandlerProtocol):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def handle(self, message: str) -> None:
        try:
            with open(self.filepath, 'a') as file:
                file.write(f'{datetime.now().isoformat()}: \t {message}\n')
        except Exception as e:
            print(f'File error: {e}')


class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

    def handle(self, message: str) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.sendall(f'{str(datetime.now().isoformat())}: \t {message}\n'.encode('utf-8'))
        except Exception as e:
            print(f'Socket error: {e}')


class ConsoleHandler(LogHandlerProtocol):
    def handle(self, message: str) -> None:
        print(f'{datetime.now().isoformat()}: \t {message}')


class SysLogHandler(LogHandlerProtocol):
    # I guess, I don't need to write a class for SysLogHandler while on Windows?..
    pass

    

class Logger:
    def __init__(self, handlers: list[LogHandlerProtocol], filters: list[LogFilterProtocol]) -> None:
        self.handlers = handlers
        self.filters = filters

    def write(self, message: str) -> None:
        if any(filter_cls.match(message) for filter_cls in self.filters):
            for handler in self.handlers:
                handler.handle(message)


                

if __name__ == '__main__':
    handlers = [
        ConsoleHandler(),
        FileHandler('Labs/Lab3/log.log'),
        SocketHandler('localhost', 5140),
    ]

    filters = [
        SimpleLogFilter('IMPORTANT'),
        SimpleLogFilter('INFO'),
        ReLogFilter(r'(ERROR|WARNING) \d+')
    ]

    logger = Logger(handlers, filters)

    messages = [
        'INFO: System started',
        'WARNING: Critical update required',
        'ERROR 404: Resource not found',
        'DEBUG: Connection established'
    ]

    for msg in messages:
        logger.write(msg)