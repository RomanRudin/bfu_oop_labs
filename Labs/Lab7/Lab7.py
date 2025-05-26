from injector import Injector, LifeStyle
from class_examples import LoggerProtocol, DatabaseProtocol, EmailServiceProtocol, ConsoleLogger, MockDatabase, MockEmailService, FileLogger, SqlDatabase, SmtpEmailService

COLORING = "\033[{}m{}\033[0m"

def configure(injector: Injector) -> None:
    injector.register(LoggerProtocol, ConsoleLogger, LifeStyle.SINGLETON)
    injector.register(DatabaseProtocol, SqlDatabase, LifeStyle.SCOPED, params={'connection_string': 'server=prod;db=app'})
    injector.register(EmailServiceProtocol, SmtpEmailService, LifeStyle.PER_REQUEST, params={'smtp_server': 'smtp.example.com'})

def demo(injector: Injector) -> None:
    #? Singleton работает везде одинаково
    logger1 = injector.get_instance(LoggerProtocol)
    logger1.log(COLORING.format(32, "Application started"))
    
    with injector.scope():
        logger2 = injector.get_instance(LoggerProtocol)
        print(COLORING.format(33, f"Same Logger instance in and ouside of scope: {logger1 is logger2}"))

        db1 = injector.get_instance(DatabaseProtocol)
        print(db1.query("SELECT * FROM users"))
        
        email1 = injector.get_instance(EmailServiceProtocol)
        print(email1.send("user@example.com", "Test", "Hello"))
        
        #? Внутри scope получаем тот же экземпляр
        db2 = injector.get_instance(DatabaseProtocol)
        print(COLORING.format(33, f"Same DB instance in scope: {db1 is db2}"))
    
    #? Вне scope - для Scoped получаем новый экземпляр
    db3 = injector.get_instance(DatabaseProtocol)
    print(COLORING.format(33, f"Same DB instance outside of scope: {db1 is db3}"))
    

    #? PerRequest всегда дает новый экземпляр
    if injector._registrations[EmailServiceProtocol]['life_style'] == LifeStyle.PER_REQUEST:
        with injector.scope():
            email2 = injector.get_instance(EmailServiceProtocol)
            email3 = injector.get_instance(EmailServiceProtocol)
            print(COLORING.format(33, f"Same EmailService instances with PerRequest: {email2 is email3}"))

if __name__ == "__main__":
    injector = Injector()
    configure(injector)
    demo(injector)