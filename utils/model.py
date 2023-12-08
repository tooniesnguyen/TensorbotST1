import torch
from torch import nn
from prettytable import PrettyTable


class Lstm_Model(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, num_layers = 1):
        super(Lstm_Model, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size , num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(self.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(self.device)

        # Ensure x has the correct dimensions
        x = x.unsqueeze(2)  # Add a dummy dimension for seq_len
        x = x.permute(0, 2, 1)  # Swap seq_len and input_size dimensions

        out, _ = self.lstm(x, (h0, c0))
        out = out[:, -1, :]  # Get only the output from the last time step
        out = self.fc(out)
        return out
    
    def count_parameter(self):
        table = PrettyTable(["Modules", "Parameters"])
        total_params = 0
        for name, parameter in self.named_parameters():
            if not parameter.requires_grad:
                continue
            param = parameter.numel()
            table.add_row([name, param])
            total_params += param
        print(table)
        print(f"Total Trainable Params: {total_params}")
        return total_params
    
    def save_model(self, model, all_words, tags, save_dir):
        data = {
        "model_state": model.state_dict(),
        "input_size": self.input_size,
        "hidden_size": self.hidden_size,
        "output_size": self.num_layers,
        "all_words": all_words,
        "tags": tags
        }
        torch.save(data, save_dir)
        print(f'training complete. file saved to {save_dir}')
        return True

if __name__ == "__main__":
    model = Lstm_Model(20, 10, 2, 10)
    model.count_parameter()
