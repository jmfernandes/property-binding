import unittest
from binding import Observer


class Coordinates(metaclass=Observer):
    x = None
    y = None

    def __init__(self, a, b):
        self.x = a
        self.y = b


def global_listener(one, two, three, four):
    pass


class ObserverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.coordinates = Coordinates(-1, 0)
        self.other_coordinates = Coordinates(99,99)
        self.one = None
        self.two = None
        self.three = None
        self.four = None

    def test_initialization_coordinates_one(self):
        self.assertEqual(self.coordinates.x, -1)
        self.assertEqual(self.coordinates.y, 0)

    def test_initialization_coordinates_two(self):
        self.assertEqual(self.other_coordinates.x, 99)
        self.assertEqual(self.other_coordinates.y, 99)

    def test_dont_overwrite_each_other(self):
        Coordinates.bind_to(Coordinates, self.listener)
        self.coordinates.x = -101
        self.coordinates.y = -102
        self.assertEqual(self.coordinates.x, -101)
        self.assertEqual(self.coordinates.y, -102)
        self.assertEqual(self.other_coordinates.x, 99)
        self.assertEqual(self.other_coordinates.y, 99)
        self.other_coordinates.x = -301
        self.other_coordinates.y = -302
        self.assertEqual(self.coordinates.x, -101)
        self.assertEqual(self.coordinates.y, -102)
        self.assertEqual(self.other_coordinates.x, -301)
        self.assertEqual(self.other_coordinates.y, -302)
        self.coordinates.x = -1
        self.coordinates.y = 0
        self.other_coordinates.x = 99
        self.other_coordinates.y = 99
        Coordinates.unbind_to(Coordinates, self.listener)

    def test_metaclass(self):
        name = self.coordinates.__class__.__name__
        dictionary = self.coordinates.__class__.__dict__
        self.assertIn(f"_{name}__observers", dictionary)
        self.assertIn("bind_to", dictionary)
        self.assertIn("unbind_to", dictionary)
        self.assertIn("get_listeners", dictionary)
        self.assertIn("has_listeners", dictionary)

    def test_binding(self):
        Coordinates.bind_to(Coordinates, global_listener)
        listener = Coordinates.get_listeners(Coordinates)
        self.assertNotEqual(listener, None)
        self.assertEqual(listener[0], global_listener)
        Coordinates.unbind_to(Coordinates, global_listener)
        listener = Coordinates.get_listeners(Coordinates)
        self.assertEqual(listener, None)

    def test_get_listener(self):
        Coordinates.bind_to(Coordinates, global_listener)
        self.assertEqual(Coordinates.get_listeners(Coordinates)[0], global_listener)
        Coordinates.unbind_to(Coordinates, global_listener)

    def test_has_listener(self):
        self.assertEqual(Coordinates.has_listeners(Coordinates), False)
        Coordinates.bind_to(Coordinates, global_listener)
        self.assertEqual(Coordinates.has_listeners(Coordinates), True)
        Coordinates.unbind_to(Coordinates, global_listener)

    def test_callback(self):
        self.assertEqual(self.one, None)
        self.assertEqual(self.two, None)
        self.assertEqual(self.three, None)
        self.assertEqual(self.four, None)
        Coordinates.bind_to(Coordinates, self.listener)
        self.coordinates.x = 1
        self.assertEqual(self.one, self.coordinates)
        self.assertEqual(self.two, "x")
        self.assertEqual(self.three, -1)
        self.assertEqual(self.four, 1)
        self.coordinates.x = -1
        Coordinates.unbind_to(Coordinates, self.listener)

    def listener(self, one, two, three, four):
        self.one = one
        self.two = two
        self.three = three
        self.four = four


if __name__ == '__main__':
    unittest.main()
