# Property Binding

## Description
This repository contains example code to set up a class to be able to broadcast changes to its properties.

## Usage
Simply have your class inherit the property binding class as a meta class. Any class variable defined with
double underscores will have a property automatically created for it. Then you can use the bind_to class method
to bind functions to changes in the class properties.

Example
```python
Class Coordinates(metaclass=Observer):
    __lat = None
    __lon = None

    def __init__(self, lat, lon):
        self.__lat = lat
        self.__lon = lon

def listener(instance, name, old_value, new_value):
    # do something here

new_coords = Coordinates(38,120)
Observer.bind_to(Coordinates, listener)
new_coords.lat = 25 # use the lat property to set the value and call listener
```

The observer.py file can either be copied into your working directory directly,
in which case you would import it as
```python
from observer import Observer
```
or you can install the Observer class globally. This will allow you to use the
Observer class anywhere on your computer without having to copy the file.
To do this, you would double click on setup.bat to install the module and then you would import it as
```python
from binding import Observer
```
Note that "binding" is the name of the module as defined in setup.py.
## Dependencies
The following libraries must be installed.

|Library                       |Version          |
|------------------------------|-----------------|
| python                       | >= 3.6.4        |
