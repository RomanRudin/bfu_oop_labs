from abc import ABC, abstractmethod
import socket
'''
#? Base
'''
class Logger(ABC):
    @abstractmethod
    def write(self, message:str) -> None:
        pass


class FileLogger(Logger):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def write(self, message: str) -> None:
        with open(self.filepath, 'w+') as file:
            file.write(f'{message}\n')

class ConsoleLogger(Logger):
    def write(self, message: str) -> None:
        print(message)

class SysLogLogger(Logger):
    pass

class SocketLogger(Logger):
    pass


# Реализация 1 (Awful inheritance)
'''
#! Class Explosion
#! количество классов равно произведению количества веток на количество реализаций
#? Плохо
                                 Logger
                            /       |       \
                        /           |            \
    ConsoleLogger, FileLogger, ...  |        FilteredLogger
                                    |
                                    |
            FilteredConsoleLogger, FilteredFileLogger...
'''
class FilteredLogger(Logger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def write(self, message: str) -> None:
        if not self.pattern in message:
            return
        super().write() # Так нельзя, абстрактный метод, но мы сейчас прсото пишем скелет

class FilteredFileLogger(Logger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
class FilteredConsoleLogger(Logger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern



# Реализация 2 (Better inheritance)
'''
#! Class Explosion
#? Всё равно плохо
                                 Logger
                            /              \
                        /                       \
    ConsoleLogger, FileLogger, ...          FilteredLogger
                                                   |             
                                                   |
                              FilteredConsoleLogger, FilteredFileLogger...
'''
class FilteredLogger(Logger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def write(self, message: str) -> None:
        if not self.pattern in message:
            return
        super().write() # Так нельзя, абстрактный метод, но мы сейчас прсото пишем скелет

class FilteredFileLogger(FilteredLogger):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def write(self, message: str) -> None:
        with open(self.filepath, 'w+') as file:
            file.write(f'{message}\n')

class FilteredConsoleLogger(FilteredLogger):
    def write(self, message: str) -> None:
        print(message)



# Реализация 3 (Multiple inheritance)
'''
#? Множественное наследование = потенциальные проблемы, поэтому не надо лучше. 
#? В нашем случае - вообще ромбовидное наследование, поэтому вообще нельзя.
'''

# Реализация 4 (One class - a lot of things)
'''
#? Вводить потенциальные возможности использования всякий фильтров в самое 
#? начало дерева наследования ведёт за собой проблемы. Один класс - одна задача.

#? В случае необходимости добавить функционал придётя лезть в код и исправлять много проблем.

#? Как только в ООП коде пишешь switch \ match - это намёк на то, что неправильно пишешь
'''
class LoggerImproved:
    def __init__(self, logger_type: str, filter_pattern: str) -> None:
        self.logger_type = logger_type
        self.filter_pattern = filter_pattern 
    def write(self, message: str) -> None:
        match self.logger_type:
            case 'File':
                pass
            case 'Console':
                print(message)
            case _:
                pass



# Реализация 5 (Composition)
'''
#? Composition - композиция, передаём фильтры, хэндлеры "на аутсорс" другим классам
#? Гибко, хорошо для тестирования, малый уровень асбтракции, 
#? принцип один класс - одна задача, легко расширяется - в общем нужно и круто!

#? Aggregation - пример: хэндлеры извне, их время жизни не ограничивается временем жизни логгера
#? Composition - пример: сщздание хэндлера в ините, время жизни ограничивается временем жизни логгера
'''
class Handler(ABC):
    @abstractmethod
    def handle(self, message: str) -> None:
        pass

class FileHandler(Handler):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def handle(self, message: str) -> None:
        with open(self.filepath, 'w+') as file:
            file.write(f'{message}\n')

class ConsoleHandler(Handler):
    def handle(self, message: str) -> None:
        print(message)

class SysLogHandler(Handler):
    def handle(self, message: str) -> None:
        print(message)

class SocketHandler(Handler):
    def __init__(self, port: str, host: str) -> None:
        pass

    def handle(self, message: str) -> None:
        print(message)


class Filter(ABC):
    @abstractmethod
    def match(self, message: str) -> bool:
        pass

class SimpleFilter(Filter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
    def match(self, message: str) -> bool:
        return self.pattern in message
    

class Logger:
    def __init__(self, handlers: list[Handler], filters: list[Filter], settings_file) -> None:
        self.handlers = handlers  # Aggregation
        self.filters = filters
        # self.format = [Format(...)]  # Composition
    def write(self, message: str) -> None:
        for filter in self.filters:
            if not filter.match(message):
                continue
            for handler in self.handlers:
                handler.handle(message)

