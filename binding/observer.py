from inspect import getfullargspec
from typing import Any, Optional, Callable


class WrongNumberOfArguments(TypeError):
    """Exception is raised when the wrong number of arguments is used."""
    pass


class Observer(type):
    """Meta class for automatically adding properties and property binding for private variables."""

    def __new__(mcs, class_name: str, bases: tuple, attrs: dict) -> type:
        for name, value in ((k, v) for k, v in attrs.items() if type(v) == type(None)):
            attrs[name] = ObserverProperty(name, class_name, f"I'm the '{name}' property.")
        attrs[f"_{class_name}__observer"] = []
        attrs["bind_to"] = mcs.bind_to
        attrs["unbind_to"] = mcs.unbind_to
        attrs["get_listener"] = mcs.get_listener
        attrs["has_listener"] = mcs.has_listener
        return type(class_name, bases, attrs)

    def bind_to(cls, callback: Callable[[Any, str, Any, Any], None]) -> None:
        """
        bind_to(callback) -> None

        Pass a function to bind_to without the parenthesis. Function must define four parameters in its definition.
        """
        args, *_ = getfullargspec(callback)
        if not ((len(args) == 5 and args[0] == "self") or (len(args) == 4 and args[0] != "self")):
            raise WrongNumberOfArguments("bind_to only accepts a function that has exactly 4 parameters for instance, "
                                         "property_name, new_value, and old_value, or 5 arguments with the first, "
                                         "argument being 'self'.")
        observers = getattr(cls, f"_{cls.__class__.__name__}__observer")
        if len(observers) > 0:
            observers.pop()
        observers.append(callback)

    def unbind_to(cls: Any) -> None:
        """
        unbind_to() -> None

        Pass a function to unbind_to without the parenthesis. Function must define four parameters in its definition.
        """
        observers = getattr(cls, f"_{cls.__class__.__name__}__observer")
        if len(observers) > 0:
            observers.pop()

    def get_listener(cls: Any) -> tuple:
        """Returns the callback functions."""
        return next(iter(getattr(cls, f"_{cls.__class__.__name__}__observer")), None)

    def has_listener(cls: Any) -> tuple:
        """Returns the callback functions."""
        return len(getattr(cls, f"_{cls.__class__.__name__}__observer")) > 0


class ObserverProperty:
    """Class for defining a custom property object."""
    stored_value = None

    def __init__(self, name: str, class_name: str, doc: Optional[str] = ...) -> None:
        self.name = name
        self.observer_list = f"_{class_name}__observer"
        self.__doc__ = doc

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Invoked when calling a property in the form obj.x

        Will set the property value and call any callback funtion.
        """
        old_value = self.stored_value
        if value != old_value:
            self.stored_value = value
            callback_functions = getattr(obj, self.observer_list)
            if len(callback_functions) > 0:
                callback_functions[0](obj, self.name, old_value, value)

    def __get__(self, obj: Any, cls: Optional[type] = ...) -> Any:
        """
        Returns the property value.
        """
        return self.stored_value
