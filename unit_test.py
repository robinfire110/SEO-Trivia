import unittest
from main import get_data, replace_invalid_characters, display_answers, check_answer
import os

class unitTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_replace_invalid_characters(self):
        self.assertEquals(replace_invalid_characters("This is a &quot;test&#039;"), "This is a \"test'")
        self.assertEquals(replace_invalid_characters("This shouldn't change"), "This shouldn't change")