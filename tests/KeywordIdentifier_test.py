from autoambience.KeywordIdentifier import KeywordIdentifier
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

    def test_identify_generators(self):
        ki = KeywordIdentifier()
        result = ki.identify_generators('We were in an airplane')
        self.assertTrue(len(result) > 0)
        self.assertTrue('Flying Fortress' in result)

        ki.soundscapes = {"Test": {"keywords": ["a", "test"]}}
        result = ki.identify_generators("This is a test")
        self.assertTrue('Test' in result)

    def test_generate_regular_link(self):
        ki = KeywordIdentifier()
        flying_fortress = ki.identify_generators('airplane')
        result = ki.generate_regular_link(flying_fortress)
        self.assertEqual(result, "http://mynoise.net/NoiseMachines/propellerNoiseGenerator.php")

        irish_coast = ki.identify_generators('coast')
        result = ki.generate_regular_link(irish_coast)
        self.assertEqual(result, "http://mynoise.net/NoiseMachines/windSeaRainNoiseGenerator.php")

    def test_generate_supergen_link(self):
        ki = KeywordIdentifier()
        flying_fortress = ki.identify_generators('It was a dark and stormy night at sea. Drifting endlessly on the coast, I had only my cat to keep me company.')
        result = ki.generate_supergen_link(flying_fortress)
        self.assertEqual(result, 'mynoise.net/superGenerator.php?g1=windSeaRainNoiseGenerator.php&g2=ultrasonicNoiseGenerator.php&g3=catPurrNoiseGenerator.php&g4=thunderNoiseGenerator.php')

    def test_process(self):
        ki = KeywordIdentifier()
        result = ki.process("This is some text about a guy and his cat and his fish")
        self.assertEqual(result, 'mynoise.net/superGenerator.php?g1=60HzFishTankNoiseGenerator.php&g2=catPurrNoiseGenerator.php')

    def test_channel_generation(self):
        ki = KeywordIdentifier()
        result = ki.generate_channels([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(result, '?c=0&l=00010203040506070809')
