from binding import Observer


class Coordinates(metaclass=Observer):
    """Any variable defined with two underscores will automatically be given a property whose name is the same as
    the variable but without the underscores."""
    x = None
    y = None

    def __init__(self, x, y):
        # initializing the variables is completely optional.
        self.x = x
        self.y = y

class Stuff():
    a = None

    def __init__(self, x, y):
        self.a = x
        self.b = y

class People(metaclass=Observer):
    name = None

    def __init__(self, n):
        self.name = n

def listener(instance, property_name, old_value, new_value):
    """Every time a property in Coordinates is changed, listener will be called."""
    print(f"listener triggered on property -> {instance} {property_name}. \n old_value: {old_value} \n new_value: {new_value}")


def main():
    # create an instance of the class.
    print("start of main")
    coord = Coordinates(2, 3)
    other_coord = Coordinates(4,5)
    john = People("John")
    # bind a function to the specific instance. An instance can be bound to an unlimited amount of functions.
    Observer.bind_to(Coordinates, listener)
    print(f"beginning coordinates are <x: {coord.x}, y: {coord.y}>")
    print(f"beginning coordinates are <x: {other_coord.x}, y: {other_coord.y}>")
    coord.x = -1
    coord.y = -5
    Observer.bind_to(People, listener)
    john.name = "larry"
    coord.x = -2
    other_coord.x = -6
    # coord.unbind_to()
    print(f"after event coordinates are <x: {coord.x}, y: {coord.y}>")
    print(f"after event coordinates are <x: {other_coord.x}, y: {other_coord.y}>")

if __name__ == "__main__":
    main()
