from utils.preprocess import Word_Processing
from utils.model import Lstm_Model
import torch
import json
import sys
import socket
import os
from pathlib import Path
import random



class NLP_Robot:
    def __init__(self, json_path, model_path):
        self.intents = self.load_json(json_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.word_process = Word_Processing()
        self.model = self.load_model(model_path)

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
    
    def chat_mode(self):
        bot_name = "Tensorbot"
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
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
            else:
                print(f"{bot_name}: I do not understand...")
            



if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[0]
    WORK_DIR = os.path.dirname(ROOT)
    
    JSON_DIR = f"{WORK_DIR}/Tensorbot/models/dicts/intents.json"
    MODEL_DIR = f"{WORK_DIR}/Tensorbot/models/best.pth"

    nlp_robot = NLP_Robot(JSON_DIR, MODEL_DIR)
    nlp_robot.chat_mode()
    
