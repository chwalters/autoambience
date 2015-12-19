from KeywordIdentifier import KeywordIdentifier
import unittest

class KeywordIdentifier_Test(unittest.TestCase):
    def test_remove_punctuation(self):
        ki = KeywordIdentifier()
        result = ki.remove_punctuation("\"This\". Is, 'something'?")
        self.assertEqual(result, "This Is something")

    def test_prepare_text_block(self):
        ki = KeywordIdentifier()
        result = ki.prepare_text_block("\"This\". Is, 'something'?")
        self.assertTrue(set(result).issubset(['this', 'is', 'something']))

    def test_match(self):
        ki = KeywordIdentifier()
        result = ki.match(['This','is','a','test'],['a', 'test', 'failure'])
        self.assertTrue(set(result).issubset(['a', 'test']))

    def test_identify(self):
        ki = KeywordIdentifier()
        ki.soundscapes = {"Test": {"keywords": ["a", "test"]}}
        result = ki.identify("This is a test")
        self.assertTrue('Test' in result)
