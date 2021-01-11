from binding import Observer


class Coordinates(metaclass=Observer):
    """Any variable defined with two underscores will automatically be given a property whose name is the same as
    the variable but without the underscores."""
    __x = None
    __y = None

    def __init__(self, x, y):
        # initializing the variables is completely optional.
        self.__x = x
        self.__y = y


def listener(instance, property_name, new_value, old_value):
    """Every time a property in Coordinates is changed, listener will be called."""
    print(f"listener triggered on property -> {property_name}")


def main():
    # create an instance of the class.
    coord = Coordinates(2, 3)
    # bind a function to the specific instance. An instance can be bound to an unlimited amount of functions.
    coord.bind_to(listener)

    print(f"beginning coordinates are <x: {coord.x}, y: {coord.y}>")
    coord.x = 1
    coord.y = 5
    print(f"after event coordinates are <x: {coord.x}, y: {coord.y}>")


if __name__ == "__main__":
    main()
