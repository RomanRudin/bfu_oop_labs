from typing import Type, Generator, Any, Callable, Optional, TypeVar
from contextlib import contextmanager

T = TypeVar('T')


class LifeStyle:
    PER_REQUEST = "PerRequest"
    SCOPED = "Scoped"
    SINGLETON = "Singleton"


class Injector:
    def __init__(self) -> None:
        self._registrations: dict[Type, dict] = {}
        self._singleton_instances: dict[Type, Any] = {}
        self._scoped_instances: dict[Type, Any] = {}
        self._in_scope = False

    def register(self,
                 interface_type: Type[T],
                 class_type: Optional[Type] = None,
                 life_style: str = LifeStyle.PER_REQUEST,
                 factory_method: Optional[Callable] = None,
                 params: Optional[dict] = None) -> None:
        if factory_method and class_type:
            raise ValueError("Cannot specify both class_type and factory_method")

        self._registrations[interface_type] = {
            'class_type': class_type,
            'life_style': life_style,
            'params': params or {},
            'factory_method': factory_method
        }

    @contextmanager
    def scope(self) -> Generator[None, Any, None]:
        if self._in_scope:
            yield
            return

        self._in_scope = True
        self._scoped_instances.clear()
        try:
            yield
        finally:
            self._in_scope = False
            self._scoped_instances.clear()

    def get_instance(self, interface_type: Type[T]) -> T:
        if interface_type not in self._registrations:
            raise ValueError(f"No registration found for {interface_type.__name__}")

        registration = self._registrations[interface_type]
        life_style = registration['life_style']

        if life_style == LifeStyle.SINGLETON:
            if interface_type in self._singleton_instances:
                return self._singleton_instances[interface_type]

            instance = self._create_instance(registration)
            self._singleton_instances[interface_type] = instance
            return instance

        if life_style == LifeStyle.SCOPED:
            if interface_type in self._scoped_instances:
                return self._scoped_instances[interface_type]

            instance = self._create_instance(registration)
            self._scoped_instances[interface_type] = instance
            return instance

        return self._create_instance(registration)

    def _create_instance(self, registration: dict) -> Any:
        if registration['factory_method']:
            return registration['factory_method']()

        class_type = registration['class_type']
        params = registration['params'].copy()

        constructor_params = {}
        if hasattr(class_type, '__annotations__'):
            for param_name, param_type in class_type.__annotations__.items():
                if param_name != 'return' and param_type in self._registrations:
                    constructor_params[param_name] = self.get_instance(param_type)

        constructor_params.update(params)

        return class_type(**constructor_params)
