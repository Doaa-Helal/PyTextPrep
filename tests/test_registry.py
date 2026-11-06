import unittest
from PyTextPrep.src import registry

class TestRegisterStep(unittest.TestCase):

    def setUp(self):
        self.original_registry = registry.STEP_REGISTRY.copy()
        registry.STEP_REGISTRY.clear()

    def tearDown(self):
        registry.STEP_REGISTRY.clear()
        registry.STEP_REGISTRY.update(self.original_registry)

    def test_register_with_custom_name(self):

        @registry.register_step("my_step")
        def example(text):
            return text

        self.assertIn("my_step", registry.STEP_REGISTRY)
        self.assertIs(registry.STEP_REGISTRY["my_step"], example)

    def test_register_with_function_name(self):

        @registry.register_step()
        def lowercase(text):
            return text.lower()

        self.assertIn("lowercase", registry.STEP_REGISTRY)

    def test_register_with_none_name(self):

        @registry.register_step(None)
        def example(text):
            return text

        self.assertIn("example", registry.STEP_REGISTRY)

    def test_register_duplicate_name(self):

        @registry.register_step("my_step")
        def first_step(text):
            return text

        with self.assertRaises(ValueError):

            @registry.register_step("my_step")
            def second_step(text):
                return text

    def test_register_empty_name(self):
        
        @registry.register_step("")
        def example(text):
            return text
        self.assertIn("example", registry.STEP_REGISTRY)

    def test_register_whitespace_name(self):
        with self.assertRaises(ValueError):
            @registry.register_step("   ")
            def example(text):
                return text

    def test_register_invalid_name_type(self):
        with self.assertRaises(ValueError):
            @registry.register_step(123)
            def example(text):
                return text

    def test_register_returns_original_function(self):
        @registry.register_step("my_step")
        def example(text):
            return text.upper()
        self.assertEqual(example("hello"), "HELLO")

class TestGetStep(unittest.TestCase):
    def setUp(self):
        self.original_registry = registry.STEP_REGISTRY.copy()
        registry.STEP_REGISTRY.clear()

    def tearDown(self):
        registry.STEP_REGISTRY.clear()
        registry.STEP_REGISTRY.update(self.original_registry)

    def test_get_existing_step(self):
        def example(text):
            return text
        registry.STEP_REGISTRY["example"] = example
        result = registry.get_step("example")
        self.assertIs(result, example)

    def test_get_nonexistent_step(self):
        with self.assertRaises(KeyError):
            registry.get_step("unknown_step")

    def test_get_step_invalid_name(self):
        with self.assertRaises(KeyError):
            registry.get_step(123)


class TestGetRegisteredSteps(unittest.TestCase):
    def setUp(self):
        self.original_registry = registry.STEP_REGISTRY.copy()
        registry.STEP_REGISTRY.clear()

    def tearDown(self):
        registry.STEP_REGISTRY.clear()
        registry.STEP_REGISTRY.update(self.original_registry)

    def test_get_registered_steps(self):
        registry.STEP_REGISTRY.update({
            "remove_digits": lambda text: text,
            "lowercase": lambda text: text,
            "remove_urls": lambda text: text
        })

        result = registry.get_registered_steps()
        self.assertEqual(
            result,
            ["lowercase", "remove_digits", "remove_urls"]
        )

    def test_empty_registry(self):
        self.assertEqual(
            registry.get_registered_steps(),
            []
        )

    def test_returns_sorted_names(self):
        registry.STEP_REGISTRY.update({
            "z_step": lambda text: text,
            "a_step": lambda text: text,
            "m_step": lambda text: text
        })
        result = registry.get_registered_steps()
        self.assertEqual(result, ["a_step", "m_step", "z_step"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
