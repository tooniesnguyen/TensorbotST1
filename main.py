from utils.preprocess import Word_Processing
from utils.model import Lstm_Model
import torch
import json
import sys
import socket
import os
from pathlib import Path



def load_model(dir_model):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    data = torch.load(dir_model)
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = len(data["tags"])
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = Lstm_Model(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    print("Load successful")
    return model


if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[0]
    WORK_DIR = os.path.dirname(ROOT)

    model = load_model(f"{WORK_DIR}/Tensorbot/models/best.pth")