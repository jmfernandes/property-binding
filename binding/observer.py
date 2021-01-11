from inspect import getfullargspec
from typing import Any, Optional, Callable


class WrongNumberOfArguments(TypeError):
    """Exception is raised when the wrong number of arguments is used."""
    pass


class Observer(type):
    """Meta class for automatically adding properties and property binding for private variables."""

    def __new__(mcs, class_name: str, bases: tuple, attrs: dict) -> type:
        for item in [x.split(f"_{class_name}__")[1] for x in attrs if x.startswith(f"_{class_name}__")]:
            attrs[item] = ObserverProperty(item, class_name, f"I'm the '{item}' property.")
        attrs[f"_{class_name}__observers"] = []
        attrs["bind_to"] = mcs.bind_to
        attrs["unbind_to"] = mcs.unbind_to
        attrs["get_listeners"] = mcs.get_listeners
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
        observers = getattr(cls, f"_{cls.__class__.__name__}__observers")
        observers.append(callback)

    def unbind_to(cls, callback: Callable[[Any, str, Any, Any], None]) -> None:
        """
        unbind_to(callback) -> None

        Pass a function to unbind_to without the parenthesis. Function must define four parameters in its definition.
        """
        observers = getattr(cls, f"_{cls.__class__.__name__}__observers")
        observers.remove(callback)

    def get_listeners(cls) -> tuple:
        """Returns a list of callback functions."""
        return tuple(getattr(cls, f"_{cls.__class__.__name__}__observers"))


class ObserverProperty:
    """Class for defining a custom property object."""

    def __init__(self, name: str, class_name: str, doc: Optional[str] = ...) -> None:
        self.name = name
        self.observer_name = f"_{class_name}__observers"
        self.value_name = f"_{class_name}__{name}"
        self.__doc__ = doc

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Invoked when calling a property in the form obj.x

        Will set the property value and call any callback funtion.
        """
        old_value = getattr(obj, self.value_name)
        if value != old_value:
            setattr(obj, self.value_name, value)
            callback_functions = getattr(obj, self.observer_name)
            for callback in callback_functions:
                callback(obj, self.name, old_value, value)

    def __get__(self, obj: Any, cls: Optional[type] = ...) -> Any:
        """
        Returns the property value.
        """
        return getattr(obj, self.value_name)
