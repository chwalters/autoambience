import json


class KeywordIdentifier:
    def __init__(self):
        with open('soundscapes.json','r') as sounds:
            self.soundscapes = json.load(sounds)

    @app.route('/process')
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
        for punc in ["\"", "'", ",", ".", "!", "?", ";", ":", "/"]:
            new_block = new_block.replace(punc,"")
        return new_block

    def prepare_text_block(self, text_block):
        '''Splits, removes punctuation, and lower-izes text'''
        without_punc = self.remove_punctuation(text_block).lower()
        return without_punc.split(" ")

    def generate_regular_link(self, soundscapes):
        link = self.soundscapes[soundscapes[0]]['url']
        return 'http://mynoise.net/NoiseMachines/' + link + '.php'

    def generate_supergen_link(self, soundscapes):
        '''Combines many sounds into one!'''
        supergen_link = 'mynoise.net/superGenerator.php?'
        number_of_soundscapes = min(len(soundscapes), 5)
        for sound_num in range(number_of_soundscapes):
            url = self.soundscapes[soundscapes[sound_num]]['url']
            supergen_link += 'g{0}={1}.php&'.format(sound_num+1, url)
        return supergen_link[:-1]
