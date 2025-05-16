from abc import ABC, abstractmethod
from typing import Generator, Type, TypeVar, Dict, Any, Callable, Optional
from contextlib import contextmanager
from injector import Injector, LifeStyle
from class_examples import ILogger, IDatabase, IEmailService, ConsoleLogger, MockDatabase, MockEmailService, FileLogger, SqlDatabase, SmtpEmailService


def configure_debug(injector: Injector) -> None:
    injector.register(ILogger, ConsoleLogger, LifeStyle.SINGLETON)
    injector.register(IDatabase, MockDatabase, LifeStyle.PER_REQUEST)
    injector.register(IEmailService, MockEmailService, LifeStyle.SCOPED)

def configure_release(injector: Injector) -> None:
    injector.register(ILogger, FileLogger, LifeStyle.SINGLETON, {'filename': 'app.log'})
    injector.register(IDatabase, SqlDatabase, LifeStyle.SCOPED, {'connection_string': 'server=prod;db=app'})
    injector.register(IEmailService, SmtpEmailService, LifeStyle.SINGLETON, {'smtp_server': 'smtp.example.com'})

def demo(injector: Injector) -> None:
    print("\n=== DEMO ===")
    
    #? Singleton работает везде одинаково
    logger = injector.get_instance(ILogger)
    logger.log("Application started")
    
    with injector.scope():
        db1 = injector.get_instance(IDatabase)
        print(db1.query("SELECT * FROM users"))
        
        email1 = injector.get_instance(IEmailService)
        print(email1.send("user@example.com", "Test", "Hello"))
        
        #? Внутри scope получаем тот же экземпляр
        db2 = injector.get_instance(IDatabase)
        print(f"Same DB instance in scope: {db1 is db2}")
    
    #? Вне scope - для Scoped получаем новый экземпляр
    try:
        db3 = injector.get_instance(IDatabase)
    except RuntimeError as e:
        print(f"Expected error outside scope: {e}")
    
    #? PerRequest всегда дает новый экземпляр
    if injector._registrations[IDatabase]['life_style'] == LifeStyle.PER_REQUEST:
        with injector.scope():
            db4 = injector.get_instance(IDatabase)
            db5 = injector.get_instance(IDatabase)
            print(f"Different DB instances with PerRequest: {db4 is not db5}")

if __name__ == "__main__":
    injector = Injector()
    
    print("DEBUG")
    configure_debug(injector)
    demo(injector)
    print()
    
    print("RELEASE")
    injector = Injector()
    configure_release(injector)
    demo(injector)