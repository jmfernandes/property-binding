from inspect import getfullargspec
from typing import Any, Optional, Callable

from binding.exceptions import WrongNumberOfArguments
from binding.decorators import static_method_decorator

class Observer(type):
    """Meta class for automatically adding properties and property binding for private variables."""

    def __new__(mcs: Any, class_name: str, bases: tuple, attrs: dict, **kwargs: dict) -> type:
        # Create a new class and store the original __init__ so it can be called later.
        new_cls = type.__new__(mcs, class_name, bases, attrs, **kwargs)
        user_init = new_cls.__init__

        # Custom init function to create instance level private variables to store values.
        def __init__(self, *args, **kwargs):
            # Create new private variable but mangle the name so users are less likely to access it.
            for item in getattr(new_cls, "properties"):
                setattr(self, f"_{class_name}__{item}", None)
            # Call the original __init__.
            user_init(self, *args, **kwargs)

        # Keep track of the Class level variables that are set to 'None' and
        # overwrite them to be custom ObserverProperty types.
        property_list = []
        for name, value in ((k, v) for k, v in attrs.items() if type(v) == type(None)):
            property_list.append(name)
            setattr(new_cls, name, ObserverProperty(name, class_name, f"I'm the '{name}' property."))

        # Set all the class level attributes.
        setattr(new_cls, '__init__', __init__)
        setattr(new_cls, 'properties', property_list)
        setattr(new_cls, f"_{class_name}__observers", [])
        setattr(new_cls, 'bind_to', mcs.bind_to)
        setattr(new_cls, 'unbind_to', mcs.unbind_to)
        setattr(new_cls, 'get_listeners', mcs.get_listeners)
        setattr(new_cls, 'has_listeners', mcs.has_listeners)
        return new_cls

    @static_method_decorator
    def bind_to(cls: Any, callback: Callable[[Any, str, Any, Any], None]) -> None:
        """
        bind_to(cls, callback) -> None

        Pass a function to bind_to without the parenthesis. Function must define four parameters in its definition.
        """
        args, *_ = getfullargspec(callback)
        if not ((len(args) == 5 and args[0] == "self") or (len(args) == 4 and args[0] != "self")):
            raise WrongNumberOfArguments("bind_to only accepts a function that has exactly 4 parameters for instance, "
                                         "property_name, new_value, and old_value, or 5 arguments with the first, "
                                         "argument being 'self'.")
        observers = getattr(cls, f"_{cls.__name__}__observers")
        observers.append(callback)

    @static_method_decorator
    def unbind_to(cls: Any, callback: Callable[[Any, str, Any, Any], None]) -> None:
        """
        unbind_to() -> None

        Pass a function to unbind_to without the parenthesis. Function must define four parameters in its definition.
        """
        observers = getattr(cls, f"_{cls.__name__}__observers")
        try:
            observers.remove(callback)
        except ValueError:
            raise ValueError(f"{callback} is not currently bound to class: {cls.__name__}")

    @static_method_decorator
    def get_listeners(cls: Any) -> tuple:
        """Returns the callback functions."""
        listeners = getattr(cls, f"_{cls.__name__}__observers")
        if not listeners:
            return None
        else:
            return tuple(listeners)

    @static_method_decorator
    def has_listeners(cls: Any) -> bool:
        """Returns the callback functions."""
        return len(getattr(cls, f"_{cls.__name__}__observers")) > 0


class ObserverProperty:
    """Class for defining a custom property object."""

    def __init__(self, name: str, class_name: str, doc: Optional[str] = ...) -> None:
        self.name = name
        self.private_value = f"_{class_name}__{name}"
        self.observer_list = f"_{class_name}__observers"
        self.__doc__ = doc

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Invoked when calling a property in the form obj.x

        Will set the property value and call any callback funtion.
        """
        old_value = getattr(obj, self.private_value)
        if value != old_value:
            setattr(obj, self.private_value, value)
            callback_functions = getattr(obj, self.observer_list)
            for callback in callback_functions:
                callback(obj, self.name, old_value, value)

    def __get__(self, obj: Any, cls: Optional[type] = ...) -> Any:
        """
        Returns the property value.
        """
        return getattr(obj, self.private_value)
