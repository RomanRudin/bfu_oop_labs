from injector import Injector, LifeStyle
from class_examples import LoggerProtocol, DatabaseProtocol, EmailServiceProtocol, ConsoleLogger, MockDatabase, \
    MockEmailService, FileLogger, SqlDatabase, SmtpEmailService

COLORING = "\033[{}m{}\033[0m"


def configure(di_container: Injector) -> None:
    di_container.register(LoggerProtocol, ConsoleLogger, LifeStyle.SINGLETON)
    di_container.register(DatabaseProtocol, SqlDatabase, LifeStyle.SCOPED,
                      params={'connection_string': 'server=prod;db=app'})
    di_container.register(EmailServiceProtocol, SmtpEmailService, LifeStyle.PER_REQUEST,
                      params={'smtp_server': 'smtp.example.com'})


def demo(di_container: Injector) -> None:
    logger1 = di_container.get_instance(LoggerProtocol)
    logger1.log(COLORING.format(32, "Application started"))

    with di_container.scope():
        logger2 = di_container.get_instance(LoggerProtocol)
        print(COLORING.format(33, f"Same Logger instance in and outside of scope: {logger1 is logger2}"))

        db1 = di_container.get_instance(DatabaseProtocol)
        print(db1.query("SELECT * FROM users"))

        email1 = di_container.get_instance(EmailServiceProtocol)
        print(email1.send("user@example.com", "Test", "Hello"))

        db2 = di_container.get_instance(DatabaseProtocol)
        print(COLORING.format(33, f"Same DB instance in scope: {db1 is db2}"))

    db3 = di_container.get_instance(DatabaseProtocol)
    print(COLORING.format(33, f"Same DB instance outside of scope: {db1 is db3}"))
    if di_container._registrations[EmailServiceProtocol]['life_style'] == LifeStyle.PER_REQUEST:
        with di_container.scope():
            email2 = di_container.get_instance(EmailServiceProtocol)
            email3 = di_container.get_instance(EmailServiceProtocol)
            print(COLORING.format(33, f"Same EmailService instances with PerRequest: {email2 is email3}"))


def configure_alternative(di_container: Injector) -> None:
    di_container.register(LoggerProtocol, FileLogger, LifeStyle.SINGLETON,
                      params={'filename': 'alternative.log'})
    di_container.register(DatabaseProtocol, MockDatabase, LifeStyle.SCOPED)
    di_container.register(EmailServiceProtocol, MockEmailService, LifeStyle.PER_REQUEST)


def demo_alternative(di_container: Injector) -> None:
    logger = di_container.get_instance(LoggerProtocol)
    logger.log("Alternative configuration started")

    with di_container.scope():
        db = di_container.get_instance(DatabaseProtocol)
        print(db.query("SELECT * FROM users"))

        email = di_container.get_instance(EmailServiceProtocol)
        print(email.send("test@example.com", "Test", "Hello"))


if __name__ == "__main__":
    # Original configuration
    main_injector = Injector()
    configure(main_injector)
    demo(main_injector)

    # Alternative configuration
    alt_injector = Injector()
    configure_alternative(alt_injector)
    demo_alternative(alt_injector)
