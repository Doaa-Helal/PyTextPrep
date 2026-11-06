
import unittest
from unittest.mock import patch
from PyTextPrep.src.pipeline import Pipeline
from PyTextPrep.src import pipeline as pipeline_module
from PyTextPrep.src.exceptions import (UnknownStepError,InvalidStepParamsError)


class TestPipelineInitialization(unittest.TestCase):

    def test_initialize_single_step(self):
        pipeline = Pipeline([("lowercase", {})])
        self.assertEqual(pipeline.steps, ["lowercase"])

    def test_initialize_multiple_steps(self):
        pipeline = Pipeline([("lowercase", {}),("normalize_whitespace", {}),("remove_digits", {})])
        self.assertEqual(pipeline.steps,["lowercase", "normalize_whitespace", "remove_digits"])

    def test_initialize_empty_pipeline(self):
        pipeline = Pipeline([])
        self.assertEqual(pipeline.steps, [])

    def test_invalid_step_name_type(self):
        with self.assertRaises(TypeError):
            Pipeline([(123, {})])

    def test_unknown_step(self):
        with self.assertRaises(UnknownStepError):
            Pipeline([("unknown_step", {})])

    def test_unknown_step_suggestion(self):
        with self.assertRaises(UnknownStepError) as context:
            Pipeline([("lowercas", {})])
        self.assertIn("lowercase", str(context.exception))

    def test_params_must_be_mapping(self):
        with self.assertRaises(TypeError):
            Pipeline([("lowercase", ["invalid"])])

    def test_invalid_step_params(self):
        with self.assertRaises(InvalidStepParamsError):
            Pipeline([("lowercase", {"invalid_parameter": True})])

    def test_valid_step_params(self):
        pipeline = Pipeline([
            ("normalize_repeating_chars", {"keep": 1})
        ])
        self.assertEqual(pipeline.steps,["normalize_repeating_chars"])


class TestPipelineTransform(unittest.TestCase):

    def test_single_step(self):
        pipeline = Pipeline([("lowercase", {})])
        result = pipeline.transform("HELLO WORLD")
        self.assertEqual(result, "hello world")

    def test_multiple_steps(self):
        pipeline = Pipeline([
            ("lowercase", {}),
            ("normalize_whitespace", {}),
            ("remove_digits", {})
        ])

        result = pipeline.transform("  HELLO   123 WORLD  ")
        self.assertEqual(result, "hello  world")

    def test_empty_pipeline(self):
        pipeline = Pipeline([])
        text = "Hello World"
        self.assertEqual(pipeline.transform(text), text)

    def test_empty_text(self):
        pipeline = Pipeline([("lowercase", {}),("normalize_whitespace", {})])
        self.assertEqual(pipeline.transform(""), "")

    def test_transform_invalid_type(self):
        pipeline = Pipeline([("lowercase", {})])
        with self.assertRaises(TypeError):
            pipeline.transform(123)

    def test_return_tokens(self):
        pipeline = Pipeline([("lowercase", {}),("normalize_whitespace", {})])
        result = pipeline.transform("HELLO   WORLD",return_tokens=True)
        self.assertEqual(result, ["hello", "world"])

    def test_return_tokens_false(self):
        pipeline = Pipeline([("lowercase", {})])
        result = pipeline.transform("HELLO WORLD",return_tokens=False)
        self.assertEqual(result, "hello world")

    def test_invalid_return_tokens_type(self):
        pipeline = Pipeline([("lowercase", {})])
        with self.assertRaises(TypeError):
            pipeline.transform("Hello", return_tokens="yes")

    def test_step_parameters_are_applied(self):
        pipeline = Pipeline([("normalize_repeating_chars", {"keep": 1})])
        result = pipeline.transform("Sooooooo")
        self.assertEqual(result, "So")


class TestPipelineReturnTypes(unittest.TestCase):

    def test_porter_stemmer_returns_list(self):
        pipeline = Pipeline([("porter_stemmer", {})])
        result = pipeline.transform("cats running")
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["cat", "run"])

    def test_invalid_step_return_type(self):
        def bad_step(text):
            return 123
        with patch.dict(pipeline_module.STEP_REGISTRY,{"bad_step": bad_step}):
            pipeline = Pipeline([("bad_step", {})])
            with self.assertRaises(TypeError) as context:
                pipeline.transform("Hello")
            self.assertIn("must return str", str(context.exception))

    def test_porter_stemmer_invalid_return_type(self):
        def bad_stemmer(text):
            return "not a list"

        with patch.dict(pipeline_module.STEP_REGISTRY,{"porter_stemmer": bad_stemmer}):
            pipeline = Pipeline([("porter_stemmer", {})])
            with self.assertRaises(TypeError) as context:
                pipeline.transform("Hello")
            self.assertIn("must return list", str(context.exception))


class TestPipelineBatch(unittest.TestCase):

    def setUp(self):
        self.pipeline = Pipeline([("lowercase", {}),("normalize_whitespace", {})])

    def test_transform_batch(self):
        texts = ["HELLO WORLD","PYTHON PROGRAMMING","MACHINE LEARNING"]
        result = self.pipeline.transform_batch(texts)
        self.assertEqual(result,["hello world","python programming","machine learning"])

    def test_transform_batch_empty_list(self):
        self.assertEqual(self.pipeline.transform_batch([]),[])

    def test_transform_batch_generator(self):
        texts = (text for text in ["HELLO", "WORLD"])
        result = self.pipeline.transform_batch(texts)
        self.assertEqual(result, ["hello", "world"])

    def test_transform_batch_with_tokens(self):
        texts = ["HELLO WORLD", "PYTHON PROGRAMMING"]
        result = self.pipeline.transform_batch(texts,return_tokens=True)
        self.assertEqual(result,[["hello", "world"],["python", "programming"]])

    def test_reject_single_string(self):
        with self.assertRaises(TypeError):
            self.pipeline.transform_batch("Hello World")

    def test_invalid_item_in_batch(self):
        texts = ["Hello", 123, "World"]
        with self.assertRaises(TypeError):
            self.pipeline.transform_batch(texts)

    def test_invalid_return_tokens_type(self):
        with self.assertRaises(TypeError):
            self.pipeline.transform_batch(
                ["Hello"],
                return_tokens="yes"
            )


class TestPipelineRepresentation(unittest.TestCase):

    def test_repr_single_step(self):
        pipeline = Pipeline([("lowercase", {})])

        self.assertEqual(repr(pipeline),"Pipeline(lowercase)")

    def test_repr_multiple_steps(self):
        pipeline = Pipeline([
            ("lowercase", {}),
            ("remove_digits", {}),
            ("normalize_whitespace", {})
        ])

        self.assertEqual(
            repr(pipeline),
            "Pipeline(lowercase -> remove_digits -> normalize_whitespace)"
        )

    def test_repr_empty_pipeline(self):
        pipeline = Pipeline([])

        self.assertEqual(repr(pipeline), "Pipeline()")


if __name__ == "__main__":
    unittest.main(verbosity=2)
