from inspect import isclass

def static_method_decorator(func):
    """Decorator function will raise error if obj.func() is called where obj is a class instance."""
    def inner_function(*args, **kwargs):
        if (len(args) == 0 or not isclass(args[0])):
            raise CannotInvokeOnInstance("This is a static class that cannot be called on an instance.")
        return func(*args, **kwargs)
    return inner_function
