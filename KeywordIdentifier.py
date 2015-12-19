import json

class KeywordIdentifier:
    def __init__(self):
        with open('soundscapes.json','r') as sounds:
            self.soundscapes = json.load(sounds)

    def identify(self, text_block):
        words = self.prepare_text_block(text_block)
        return [s for s in self.soundscapes if self.match(text_block, self.soundscapes[s]['keywords'])]

    def match(self, check, check_against):
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
