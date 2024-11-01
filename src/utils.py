from model import BertClassifier
import json 
import torch 
import pandas as pd
import warnings

def load_intents(data_path):
    with open(data_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data['intents'])
    return df

def load_labels(labels_path):
    with open(labels_path) as f:
        labels = json.load(f)
    return labels

def load_model(n_classes, checkpoint_path):
    model = BertClassifier(n_classes)
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model = model.to(device)
    return model