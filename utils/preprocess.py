import numpy as np
import nltk
nltk.download('wordnet')

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except:
    nltk.download('punkt')
    nltk.download('wordnet')   
from nltk.stem.wordnet import WordNetLemmatizer

class Word_Processing:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, sentence):
        return nltk.word_tokenize(sentence)
    
    def lemma(self, word):
        return self.lemmatizer.lemmatize(word.lower())
    
    def bag_words(self, tokenized_sentence, words):
        sentence_words = [self.lemma(word) for word in tokenized_sentence]
        bag = np.zeros(len(words), dtype=np.float32)
        for idx, w in enumerate(words):
            if w in sentence_words: 
                bag[idx] = 1
        return bag
    
if __name__ == "__main__":
    word_process = Word_Processing()
    print(word_process.lemma("Goes"))
