import numpy as np
import json
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from transformers import BertTokenizer
device = torch.device('cuda')
import torch.nn.functional as F
import argparse
import torch
from utils import load_intents, load_labels, load_model
from engine import match_case
from requests.exceptions import ChunkedEncodingError
import os
import sys

os.environ["TRANSFORMERS_OFFLINE"] = "1"

def predict(model, tokenizer, text, max_length=20):
    text_dict = tokenizer(text, padding='max_length', max_length = max_length, truncation=True, return_tensors="pt")
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    model = model.to(device)
    mask = text_dict['attention_mask'].to(device)
    input_id = text_dict['input_ids'].squeeze(1).to(device)
        
    with torch.no_grad():
        output = model(input_id, mask)
        
        # Aplica softmax para converter logits em probabilidades
        probabilities = F.softmax(output, dim=1)
        
        # Encontra o índice (id da classe) com a maior probabilidade
        label_id = probabilities.argmax(dim=1).item()
        
        # Obtem a probabilidade máxima (associada à classe predita)
        max_prob = probabilities.max(dim=1).values.item()

        return label_id, max_prob, probabilities


def chat_loop(model, tokenizer, df, labels, max_length=20):
    intents = []
    tokenizer = AutoTokenizer.from_pretrained("lfcc/bert-portuguese-ner")
    ner_model = AutoModelForTokenClassification.from_pretrained("lfcc/bert-portuguese-ner")
    if os.path.isdir('hf_cache/'):
        ner_classifier = pipeline(
        "token-classification",
        model=ner_model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1, # 0 para CUDA, -1 para CPU
        model_kwargs={"cache_dir": 'hf_cache/', 'local_files_only': True})
    else: 
        os.mkdir('hf_cache/')
        ner_classifier = pipeline(
        "token-classification",
        model=ner_model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,  # 0 para CUDA, -1 para CPU
        model_kwargs={"cache_dir": 'hf_cache/', 'force_download': True})
        
    sys.stdout.flush()
    sys.stderr.flush()
    result_flag = None
    while True:
        try:
            # Take user input
            inp = input("You: ")
            if inp.lower() == "quit":
                print("Te vejo em breve amigo(a)!")
                break
            
            prediction, max_prob, probabilities = predict(model, tokenizer, inp)
            if max_prob <= 0.10:
                print("Bot: Desculpe, não entendi o que você disse. Pode falar resumidamente e de forma clara?")
                continue
            
            intent = "Fallback"
            for i in labels:
                if labels[i]==prediction:
                    intent=i
                    intents.append(i)
                    
                    if(result_flag == "Saudação"):
                        if(intent == "RecebimentoDeLocalizacao"):
                            i = "RespostaSaudação"
                        result_flag = None
                        
                    if(intent == "Saudação"):
                        result_flag = "Saudação"    

                    result = match_case(i, ner_classifier, inp, df)
                    if result == "ConsultaUltimosIntents":
                        print("Bot: Últimos intents: ", intents[-3:])

        except ChunkedEncodingError:
            sys.stdout.flush()
            sys.stderr.flush()      
            pass  
        except Exception as e:
            sys.stdout.flush()
            sys.stderr.flush()
            pass 
            
def main(args):
    
    checkpoint_path = args.checkpoint_path
    labels = args.labels
    data = args.data
    labels = load_labels(labels)
    n_classes = len(labels)
    
    model = load_model(n_classes, checkpoint_path)  
    tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', max_length=20, padding='max_length', truncation=True)
    df = load_intents(data)
    chat_loop(model, tokenizer, df, labels)
    
    
if __name__ == '__main__':
    # parser to ger the checkpoint path
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--checkpoint_path', type=str, required=True)
    parser.add_argument('-d', '--data', type=str, required=True)
    parser.add_argument('-l', '--labels', type=str, required=True)
    args = parser.parse_args()
    
    main(args)