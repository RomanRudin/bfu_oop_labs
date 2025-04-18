
#? Facade pattern

class HeatingController:
    def increase(self, temp: int) -> None:
        ...
    def decrease(self, temp: int) -> None:
        ...

class LightController:
    def turn_on(self) -> None:
        ...
    def turn_off(self) -> None:
        ...

class CurtainCOntroller:
    def open(self, percentage: int) -> None:
        ...


class RemoteControl:
    def __init__(self) -> None:
        self.heating_controller = HeatingController()
        self.light_controller = LightController()
        self.curtain_controller = CurtainCOntroller()

    def increase_temperature(self, temp: int) -> None:
        self.heating_controller.increase(temp)
    def decrease_temperature(self, temp: int) -> None:
        self.heating_controller.decrease(temp)

    def turn_on_light(self) -> None:
        self.light_controller.turn_on()
    def turn_off_light(self) -> None:
        self.light_controller.turn_off()

    def open_curtain(self, percentage: int) -> None:
        self.curtain_controller.open(percentage)

if __name__ == "__main__":
    remote_control = RemoteControl()
    remote_control.increase_temperature(10)
    remote_control.open_curtain(20)



#? Adapter pattern

from dataclasses import dataclass
from typing import Any

@dataclass
class User:
    id: int
    name: str

class OldService:
    def fetch_from_db(self) -> Any:
        ...

class KlassA:
    def method_a(self):
        ...

# Other example:
class KlassB:
    def method_b(self):
        ...

class AdapterOfOldService:
    def __init__(self) -> None:
        self.old_service = OldService()

class KlassBAdapter:
    def __init__(self, KlassB: KlassB) -> None:
        self.klass_b = KlassB
    def method_a(self):
        ...

if __name__ == "__main__":
    # data = [KlassA(), KlassB()]
    data = [KlassA(), KlassBAdapter(KlassB())]
    for item in data:
        item.method_a()



#? Decorator pattern
from datetime import datetime

class Logger:
    def log(self, message: str) -> None:
        print(message)

@dataclass
class Order:
    time: datetime
    number: int
    table_number: int

class OrderService:
    def make_order(self, orde: Order) -> None:
        ...

class LoggerDecorator: # Pattern-decorator
    def __init__(self, order_service: OrderService, logger: Logger) -> None:
        self.order_service = order_service #It should be done with any possible service, not only order_service
        self.logger = logger

    def make_order(self, order: Order) -> None:
        self.logger.log("Order started")
        self.order_service.make_order(order)
        self.logger.log("Order finished")

from time import perf_counter
from functools import wraps

def timeit(func: callable) -> callable: # Function-decorator
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        print(f"Time: {end - start}")
        return res
    return wrapper

class Timeit: # Class-decorator
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

@timeit
def test_func():
    print('fmdsjfnjojf')

if __name__ == "__main__":
    test_func()



#? Proxy pattern
# Quite easy



#? Composite pattern: component, leaf, branch
# Form, Panel, TextEdit, Lable, Button, SpinEdit, ComboBox



#? Flyweight pattern
# For changing behaviour (especially for initialization process, especialy when the object is large)



#? Injection of controls: (Not a pattern, but will be in lab)

from enum import Enum

class LifeTime(Enum):
    PER_REQUEST = 1,
    PER_APP = 2

class Injector:
    def __init__(self) -> None:
        self.registered_items = {}
    def register_class(self, interface_type, class_type, life_time: LifeTime) -> None:
        self.registered_items[interface_type] = class_type

    def get_instance(self, interface_type) -> class_type:
        ...



#? bridge pattern

