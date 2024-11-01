import torch.nn as nn
from transformers import BertModel
class BertClassifier(nn.Module):

    def __init__(self, n_classes, dropout=0.2):

        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, n_classes)

    def forward(self, input_id, mask):

        _, pooled_output = self.bert(input_ids= input_id, attention_mask=mask,return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)


        return (linear_output)