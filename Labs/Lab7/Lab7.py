from injector import Injector, LifeStyle
from class_examples import LoggerProtocol, DatabaseProtocol, EmailServiceProtocol, ConsoleLogger, MockDatabase, MockEmailService, FileLogger, SqlDatabase, SmtpEmailService


def configure_debug(injector: Injector) -> None:
    injector.register(LoggerProtocol, ConsoleLogger, LifeStyle.SINGLETON)
    injector.register(DatabaseProtocol, MockDatabase, LifeStyle.PER_REQUEST)
    injector.register(EmailServiceProtocol, MockEmailService, LifeStyle.SCOPED)

def configure_release(injector: Injector) -> None:
    injector.register(LoggerProtocol, FileLogger, LifeStyle.SINGLETON, params={'filename': 'app.log'})
    injector.register(DatabaseProtocol, SqlDatabase, LifeStyle.SCOPED, params={'connection_string': 'server=prod;db=app'})
    injector.register(EmailServiceProtocol, SmtpEmailService, LifeStyle.SINGLETON, params={'smtp_server': 'smtp.example.com'})

def demo(injector: Injector) -> None:
    print()
    print("DEMO")
    
    #? Singleton работает везде одинаково
    logger = injector.get_instance(LoggerProtocol)
    logger.log("Application started")
    
    with injector.scope():
        db1 = injector.get_instance(DatabaseProtocol)
        print(db1.query("SELECT * FROM users"))
        
        email1 = injector.get_instance(EmailServiceProtocol)
        print(email1.send("user@example.com", "Test", "Hello"))
        
        #? Внутри scope получаем тот же экземпляр
        db2 = injector.get_instance(DatabaseProtocol)
        print(f"Same DB instance in scope: {db1 is db2}")
    
    #? Вне scope - для Scoped получаем новый экземпляр
    try:
        db3 = injector.get_instance(DatabaseProtocol)
    except RuntimeError as e:
        print(f"Expected error outside scope: {e}")
    
    #? PerRequest всегда дает новый экземпляр
    if injector._registrations[DatabaseProtocol]['life_style'] == LifeStyle.PER_REQUEST:
        with injector.scope():
            db4 = injector.get_instance(DatabaseProtocol)
            db5 = injector.get_instance(DatabaseProtocol)
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