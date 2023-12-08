import numpy as np
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')   
from nltk.stem.porter import PorterStemmer

class Word_Processing:
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()

    def tokenize(self, sentence):
        return nltk.word_tokenize(sentence)
    
    def stem(self, word):
        return self.stemmer.stem(word.lower())
    
    def bag_words(self, tokenized_sentence, words):
        sentence_words = [self.stem(word) for word in tokenized_sentence]
        bag = np.zeros(len(words), dtype=np.float32)
        for idx, w in enumerate(words):
            if w in sentence_words: 
                bag[idx] = 1
        return bag
    

