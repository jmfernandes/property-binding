import argparse
import datetime
import random
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

class Map():
    """Example class that does not have any Observer binding. This is used for testing."""
    def __init__(self, x, y):
        self.lat = x
        self.lon = y

class People(metaclass=Observer):
    """This is a second class with the Observer metaclass. This is used for testing"""
    name = None

    def __init__(self, n):
        self.name = n

def listener(instance, property_name, old_value, new_value):
    """Every time a property in Coordinates is changed, listener will be called."""
    print(f"listener triggered on property -> {instance} {property_name}. \n old_value: {old_value} \n new_value: {new_value}")

def empty_listener(a, b, c, d):
    """This is used for testing"""
    pass

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

def clocktest():
    number_of_writes = 10000
    number_of_runs = 10
    map_object = Map(0,0)
    sum = 0
    for i in range(number_of_runs):
        start = datetime.datetime.now()
        for i in range(number_of_writes):
            map_object.lat = random.randint(1,1000)
        end = datetime.datetime.now()
        sum += (end - start).total_seconds()
    map_difference = sum / number_of_runs
    print("total time for Map =", map_difference)
    ##
    coord = Coordinates(0,0)
    sum = 0
    for i in range(number_of_runs):
        start = datetime.datetime.now()
        for i in range(number_of_writes):
            coord.x = random.randint(1,1000)
        end = datetime.datetime.now()
        sum += (end - start).total_seconds()
    unbound_difference = sum / number_of_runs
    percent_difference = (unbound_difference - map_difference) / map_difference * 100
    print("total time for unbound Coordinates =", unbound_difference, "percent increase =", percent_difference)
    ##
    coord = Coordinates(0,0)
    Observer.bind_to(Coordinates, empty_listener)
    sum = 0
    for i in range(number_of_runs):
        start = datetime.datetime.now()
        for i in range(number_of_writes):
            coord.x = random.randint(1,1000)
        end = datetime.datetime.now()
        sum += (end - start).total_seconds()
    Observer.unbind_to(Coordinates, empty_listener)
    bound_difference = sum / number_of_runs
    percent_difference = (bound_difference - map_difference) / map_difference * 100
    print("total time for bound Coordinates =", bound_difference, "percent increase =", percent_difference)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clock', action='store_true', help="Set flag to run clocking test")
    return(parser.parse_args())


if __name__ == "__main__":
    args = get_arguments()
    if args.clock:
        clocktest()
    else:
        main()
