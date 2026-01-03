import unittest
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bmi_mcp_server import greet


class TestGreetFunction(unittest.TestCase):
    """Unit tests for the greet function"""

    def test_greet_with_default_name(self):
        """Test greet with default 'World' parameter"""
        result = greet()
        self.assertEqual(result["message"], "Hello, World!")
        self.assertEqual(result["name"], "World")

    def test_greet_with_custom_name(self):
        """Test greet with a custom name"""
        result = greet("Alice")
        self.assertEqual(result["message"], "Hello, Alice!")
        self.assertEqual(result["name"], "Alice")

    def test_greet_with_multiple_words(self):
        """Test greet with a name containing multiple words"""
        result = greet("John Doe")
        self.assertEqual(result["message"], "Hello, John Doe!")
        self.assertEqual(result["name"], "John Doe")

    def test_greet_with_whitespace(self):
        """Test greet with a name containing leading/trailing whitespace"""
        result = greet("  Bob  ")
        self.assertEqual(result["message"], "Hello, Bob!")
        self.assertEqual(result["name"], "Bob")

    def test_greet_with_empty_string(self):
        """Test greet with an empty string"""
        result = greet("")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Name must be a non-empty string")

    def test_greet_with_whitespace_only(self):
        """Test greet with whitespace-only string"""
        result = greet("   ")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Name must be a non-empty string")

    def test_greet_with_non_string_type(self):
        """Test greet with non-string input"""
        result = greet(123)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Name must be a non-empty string")

    def test_greet_with_none(self):
        """Test greet with None"""
        result = greet(None)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Name must be a non-empty string")

    def test_greet_with_special_characters(self):
        """Test greet with special characters in name"""
        result = greet("José")
        self.assertEqual(result["message"], "Hello, José!")
        self.assertEqual(result["name"], "José")


if __name__ == "__main__":
    unittest.main()
