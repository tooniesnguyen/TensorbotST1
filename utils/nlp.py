from .preprocess import Word_Processing
from .model import Lstm_Model
import torch
import json
import sys
import socket
import os
from pathlib import Path
import random
import time

HOST = socket.gethostbyname(socket.gethostname())
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
WORK_DIR = os.path.dirname(ROOT)

JSON_DIR = f"{WORK_DIR}/data/dicts/intents.json"
MODEL_DIR = f"{WORK_DIR}/models/best.pth"


def time_complexity(func):
    def warp(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Time inference func {func.__name__}: {(time.time() - start):.3f} second')
        return result
    return warp

class Tensorbot:
    def __init__(self, json_path = JSON_DIR, model_path = MODEL_DIR):
        self.intents = self.load_json(json_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.word_process = Word_Processing()
        self.model = self.load_model(model_path)
        self.bot_name = "Tensorbot"

    def load_json(self, json_path):
        with open(json_path, 'r') as json_data:
            intents = json.load(json_data)
        return intents

    def load_model(self, model_path):
        data = torch.load(model_path)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = len(data["tags"])
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        model = Lstm_Model(input_size, hidden_size, output_size).to(self.device)
        model.load_state_dict(model_state)
        model.eval()
        print("Load successful")
        return model
    
    # @time_complexity
    def feed_back(self, sentence):
        sentence = self.word_process.tokenize(sentence)
        X = self.word_process.bag_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)
        
        output = self.model(X)
        _, predicted = torch.max(output, dim = 1)

        tag = self.tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    text = random.choice(intent['responses'])
        else:
            text = "I do not understand you"
            
        return text, tag

    

    def chat_mode(self):
        while True:
            sentence = input("You: ")
            if sentence == "quit":
                break
            sentence = self.word_process.tokenize(sentence)
            X = self.word_process.bag_words(sentence, self.all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(self.device)
            
            output = self.model(X)
            _, predicted = torch.max(output, dim=1)

            tag = self.tags[predicted.item()]
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            if prob.item() > 0.75:
                for intent in self.intents['intents']:
                    if tag == intent["tag"]:
                        print(f"{self.bot_name}: {random.choice(intent['responses'])}")
            else:
                print(f"{self.bot_name}: I do not understand...")
            
    def speech_mode(self):
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout = 5)
            try:
                sentence = recognizer.recognize_google(audio)
                print("You said:", sentence)
                sentence = self.word_process.tokenize(sentence)
                X = self.word_process.bag_words(sentence, self.all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(self.device)
                
                output = self.model(X)
                _, predicted = torch.max(output, dim=1)

                tag = self.tags[predicted.item()]
                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]
                if prob.item() > 0.75:
                    for intent in self.intents['intents']:
                        if tag == intent["tag"]:
                            print(f"{self.bot_name}: {random.choice(intent['responses'])}")
                else:
                    print(f"{self.bot_name}: I do not understand...")
            except sr.UnknownValueError:
                print("Sorry, I could not understand.")

class controller_tensorbot:
    pass


if __name__ == "__main__":

    tensorbot = Tensorbot()
    tensorbot.chat_mode()
    # print(tensorbot.feed_back("Hello"))