
class WrongNumberOfArguments(TypeError):
    """Exception is raised when the wrong number of arguments is used."""
    pass

class CannotInvokeOnInstance(TypeError):
    """Exception is raised when a static class is called from an instance."""
    pass
