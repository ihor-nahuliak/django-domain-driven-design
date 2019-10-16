import unittest
from dataclasses import dataclass, is_dataclass

from app.core import entities


class TestCase(unittest.TestCase):

    def setUp(self):
        @dataclass
        class Thing(entities.Entity):
            mandatory: int
            optional: int = 1

        @dataclass
        class UnregisteredExtra:
            mandatory: int
            optional: int = 1

        @dataclass
        class RegisteredExtra:
            mandatory: int
            optional: int = 1

        entities.register(RegisteredExtra)

        self.Thing = Thing
        self.UnregisteredExtra = UnregisteredExtra
        self.RegisteredExtra = RegisteredExtra

    def test_hierarchy_class_is_dataclass(self):
        self.assertTrue(is_dataclass(self.Thing))

    def test_hierarchy_class_instance_is_dataclass(self):
        thing = self.Thing(mandatory=1)

        self.assertTrue(is_dataclass(thing))

    def test_hierarchy_class_is_a_subclass_of_abstract_entity(self):
        self.assertTrue(issubclass(self.Thing, entities.Entity))

    def test_hierarchy_class_instance_is_an_instance_of_abstract_entity(self):
        thing = self.Thing(mandatory=1)

        self.assertTrue(isinstance(thing, entities.Entity))

    def test_unregistered_class_is_dataclass(self):
        self.assertTrue(is_dataclass(self.UnregisteredExtra))

    def test_unregistered_class_instance_is_dataclass(self):
        extra = self.UnregisteredExtra(mandatory=1)

        self.assertTrue(is_dataclass(extra))

    def test_unregistered_class_is_not_a_subclass_of_abstract_entity(self):
        self.assertFalse(issubclass(self.UnregisteredExtra, entities.Entity))

    def test_unregistered_class_instance_is_not_an_instance_of_abstract_entity(self):
        extra = self.UnregisteredExtra(mandatory=1)

        self.assertFalse(isinstance(extra, entities.Entity))

    def test_registered_class_is_dataclass(self):
        self.assertTrue(is_dataclass(self.RegisteredExtra))

    def test_registered_class_instance_is_dataclass(self):
        extra = self.RegisteredExtra(mandatory=1)

        self.assertTrue(is_dataclass(extra))

    def test_registered_class_is_a_subclass_of_abstract_entity(self):
        self.assertTrue(issubclass(self.RegisteredExtra, entities.Entity))

    def test_registered_class_instance_is_an_instance_of_abstract_entity(self):
        extra = self.RegisteredExtra(mandatory=1)

        self.assertTrue(isinstance(extra, entities.Entity))


if __name__ == '__main__':
    unittest.main()
