from bs4 import BeautifulSoup
import unittest
import keyword_manager

class TestKeywordManager(unittest.TestCase):
    def setUp(self):
        self.km = keyword_manager.KeywordManager()

    def test_is_keyword_valid_with_valid_keyword(self):
        self.assertTrue(self.km.is_keyword_valid("validkeyword"))

    def test_is_keyword_valid_with_empty_string(self):
        self.assertFalse(self.km.is_keyword_valid(""))

    def test_is_keyword_valid_with_whitespace_string(self):
        self.assertFalse(self.km.is_keyword_valid("   "))

    def test_is_keyword_valid_with_non_string(self):
        self.assertFalse(self.km.is_keyword_valid(123))
        self.assertFalse(self.km.is_keyword_valid(None))
        self.assertFalse(self.km.is_keyword_valid([]))

    def test_is_invalid_keyword_with_valid_keyword(self):
        self.assertFalse(self.km.is_invalid_keyword("validkeyword"))

    def test_is_invalid_keyword_with_empty_string(self):
        self.assertTrue(self.km.is_invalid_keyword(""))

    def test_is_invalid_keyword_with_whitespace_string(self):
        self.assertTrue(self.km.is_invalid_keyword("   "))

    def test_is_invalid_keyword_with_non_string(self):
        self.assertTrue(self.km.is_invalid_keyword(123))
        self.assertTrue(self.km.is_invalid_keyword(None))
        self.assertTrue(self.km.is_invalid_keyword([]))

    def test_process_keywords(self):
        self.km.keywords = ["ValidKeyword", "  ", "", "AnotherKeyword", 123, None]
        self.km.process_keywords()
        self.assertEqual(self.km.get_keywords(), ["validkeyword", "anotherkeyword"])

if __name__ == '__main__':
    unittest.main()