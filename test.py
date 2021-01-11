import unittest
from binding import Observer


class Coordinates(metaclass=Observer):
    __x = -1
    __y = None


def global_listener(one, two, three, four):
    pass


class ObserverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.coordinates = Coordinates()
        self.one = None
        self.two = None
        self.three = None
        self.four = None

    def test_initialization(self):
        self.assertEqual(self.coordinates.x, -1)
        self.assertEqual(self.coordinates.y, None)

    def test_metaclass(self):
        name = self.coordinates.__class__.__name__
        dictionary = self.coordinates.__class__.__dict__
        self.assertIn(f"_{name}__observers", dictionary)
        self.assertIn("bind_to", dictionary)
        self.assertIn("unbind_to", dictionary)
        self.assertIn("get_listeners", dictionary)

    def test_binding(self):
        self.coordinates.bind_to(global_listener)
        listeners = self.coordinates.get_listeners()
        self.assertEqual(len(listeners), 1)
        self.assertEqual(listeners[0], global_listener)
        self.coordinates.unbind_to(global_listener)
        listeners = self.coordinates.get_listeners()
        self.assertEqual(len(listeners), 0)

    def test_callback(self):
        self.assertEqual(self.one, None)
        self.assertEqual(self.two, None)
        self.assertEqual(self.three, None)
        self.assertEqual(self.four, None)
        self.coordinates.bind_to(self.listener)
        self.coordinates.x = 1
        self.assertEqual(self.one, self.coordinates)
        self.assertEqual(self.two, "x")
        self.assertEqual(self.three, -1)
        self.assertEqual(self.four, 1)
        self.coordinates.unbind_to(self.listener)

    def listener(self, one, two, three, four):
        self.one = one
        self.two = two
        self.three = three
        self.four = four


if __name__ == '__main__':
    unittest.main()
