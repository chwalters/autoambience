import json, random

class KeywordIdentifier:
    regular_channel_prefix = '?c=0&l='
    supergen_channel_prefix = '%3Fc%3D3%26l%3D'
    regular_url = 'http://mynoise.net/NoiseMachines/{0}.php'
    supergen_url = 'mynoise.net/superGenerator.php?'
    supergen_joiner = 'g{0}={1}.php{2}&'

    def __init__(self):
        self.punctuation = ["\"", "'", ",", ".", "!", "?", ";", ":", "/"]
        with open('soundscapes.json','r') as sounds:
            self.soundscapes = json.load(sounds)

    def process(self, text_block):
        '''Main feature; takes a block of text, then generates supergen'''
        generators = self.identify_generators(text_block)
        return self.generate_supergen_link(generators)

    def identify_generators(self, text_block):
        '''Looks through each soundscape to find keyword matches'''
        words = self.prepare_text_block(text_block)
        return [s for s in self.soundscapes if self.match(words, self.soundscapes[s]['keywords'])]

    def match(self, check, check_against):
        '''Helper method; intersects two lists'''
        return list(filter(lambda x: x in check_against, check))

    def remove_punctuation(self, text_block):
        '''Removes all punctuation from a string'''
        new_block = text_block
        for punc in self.punctuation:
            new_block = new_block.replace(punc,"")
        return new_block

    def prepare_text_block(self, text_block):
        '''Splits, removes punctuation, and lower-izes text'''
        without_punc = self.remove_punctuation(text_block).lower()
        return without_punc.split(" ")

    def generate_regular_link(self, soundscapes, amplitudes=None):
        soundscape_url = self.soundscapes[soundscapes[0]]['url']
        regular_link =  KeywordIdentifier.regular_url.format(soundscape_url)
        if amplitudes is not None:
            channel_link = self.generate_channels(self.regular_channel_prefix, amplitudes)
            return regular_link + channel_link
        return regular_link

    def generate_supergen_link(self, soundscapes):
        '''Combines many sounds into one!'''
        supergen_link = ''
        number_of_soundscapes = min(len(soundscapes), 5)
        for sound_num in range(number_of_soundscapes):
            generator_url = self.soundscapes[soundscapes[sound_num]]['url']
            channel_text = '' # TBD
            supergen_link += KeywordIdentifier.supergen_joiner.format(sound_num+1, generator_url, channel_text)
        full_url = KeywordIdentifier.supergen_url + supergen_link[:-1]
        return full_url

    def generate_channels(self, channel_prefix, amplitudes):
        '''Uses a 10-Dim vector to specify per-channel amplitudes'''
        channel_text = ''.join('{0:02d}'.format(x) for x in amplitudes)
        return channel_prefix + channel_text

    def random(self):
        '''Used for training'''
        rand_gen_number = random.randint(0, len(self.soundscapes))
        rand_gen_id  = [gen for gen in self.soundscapes][rand_gen_number]
        randomized_amplitudes = [random.randint(0, 99) for x in range(10)]
        return self.generate_regular_link([rand_gen_id], randomized_amplitudes)
