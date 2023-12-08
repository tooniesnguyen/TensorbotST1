from preprocess import Word_Processing
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import Lstm_Model
import sys
import socket
import os
from pathlib import Path




class Data_Preprocessing:
    def __init__(self, json_dir) -> None:
        self.content_json = self.load_json(json_dir)
        self.word_process = Word_Processing()
        self.all_words =[]
        self.tags = []
        self.data = []

    def load_json(self, json_dir):
        with open(json_dir, 'r') as f:
            return json.load(f)

    def create_data(self):
        ignore_words = ['?', '.', '!', '*']
        for content in self.content_json['intents']:
            tag = content['tag']
            self.tags.append(tag)
            for pattern in content["patterns"]:
                word = self.word_process.tokenize(pattern)
                self.all_words.extend(word)
                self.data.append([word, tag])
        self.all_words = [self.word_process.stem(w) for w in self.all_words if w not in ignore_words]
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(set(self.tags))
        return self.all_words, self.tags, self.data
    
    def X_y_split(self):
        X = []
        y = []
        for (pattern_sentence, tag) in self.data:
            bag = self.word_process.bag_words(pattern_sentence, self.all_words)
            X.append(bag)
            label = self.tags.index(tag)
            y.append(label)
        X = np.array(X)
        y = np.array(y)
        return X, y
    
class ChatDataset(Dataset):
    def __init__(self, X_train, y_train):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

def main():
    json_dir = "/home/toonies/Learn/Tensorbot/models/dicts/intents.json"
    data_process = Data_Preprocessing(json_dir)
    all_words, tags, _ =data_process.create_data()
    X_train, y_train = data_process.X_y_split()
    print("X_shape", X_train.shape)
    num_epochs = 3000
    batch_size = 8
    learning_rate = 0.001
    input_size = len(X_train[0])
    hidden_size = 8
    output_size = len(tags)
    dataset = ChatDataset(X_train, y_train)
    train_loader = DataLoader(dataset=dataset,
                            batch_size=batch_size,
                            shuffle=True,
                            num_workers=0)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Lstm_Model(input_size, hidden_size, output_size).to(device)
    model.count_parameter()

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(dtype=torch.long).to(device)
            
            # Forward pass
            outputs = model(words)

            loss = criterion(outputs, labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
        if (epoch+1) % 1000 == 0:
            print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    print(f'final loss: {loss.item():.4f}')
    model.save_model(model, all_words, tags, f"{WORK_DIR}/models/best.pth")

    
if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[0]
    WORK_DIR = os.path.dirname(ROOT)

    main()
