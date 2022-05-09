# Property Binding

## Description
This repository contains example code to set up a class to be able to broadcast changes to its properties.

## Usage
Simply have your class inherit the 'Observer' class as a meta class. Any class variables that are set to 'None' will have a property automatically created for it. Then you can use the 'bind_to' class method to bind callback functions to changes in the class properties. The 'bind_to' method cannot be called on instances of a class, only on the Observer class itself. Same goes for the 'unbind_to', 'has_listeners', and 'get_listeners' functions.

Example
```python
from binding import Observer

Class Coordinates(metaclass=Observer):
    # These two class variables (lat and lon) will be turned into properties.
    # Property values are specific to each instance so you can create as many
    # instances as you want. The values will not overwrite each other.
    lat = None
    lon = None
    # map_type will NOT be turned into a property.
    map_type = "2D"

    def __init__(self, lat, lon):
        # You are free to initialize each instance however you want.
        # In this example, any bound callback functions will be called twice:
        # once for the lat variable and once for the lon variable.
        self.lat = lat
        self.lon = lon

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
