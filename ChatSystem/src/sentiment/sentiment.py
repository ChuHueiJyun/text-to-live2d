import os
import torch
import pickle
import numpy as np
from torch import nn
from sklearn import metrics
from transformers import DistilBertTokenizer, DistilBertModel

class MyModel(nn.Module):
    def __init__(self, ndim=64, edim=64, cdim=1):
        super(MyModel, self).__init__()

        # song embedding
        self.spec_bn = nn.BatchNorm2d(1)
        self.layer1 = Conv_2d(1, ndim, pooling=2)
        self.layer2 = Res_2d_mp(ndim, ndim, pooling=2)
        self.layer3 = Conv_2d(ndim, ndim*2, pooling=2)
        self.layer4 = Res_2d_mp(ndim*2, ndim*2, pooling=2)
        self.layer5 = Res_2d_mp(ndim*2, ndim*2, pooling=2)
        self.layer6 = Res_2d_mp(ndim*2, ndim*2, pooling=(2,3))
        self.layer7 = Conv_2d(ndim*2, ndim*4, pooling=(2,3))
        self.layer8 = Conv_emb(ndim*4, ndim*4)
        self.song_fc1 = nn.Linear(ndim*4, ndim*2)
        self.song_bn = nn.BatchNorm1d(ndim*2)
        self.song_fc2 = nn.Linear(ndim*2, edim)

        # text embedding
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased', return_dict=True)
        self.bert.train()
        self.text_fc1 = nn.Linear(768, ndim*2)
        self.text_bn = nn.BatchNorm1d(ndim*2)
        self.text_fc2 = nn.Linear(ndim*2, edim)

        # tag embedding
        self.tag_fc1 = nn.Linear(300, ndim*2)
        self.tag_bn = nn.BatchNorm1d(ndim*2)
        self.tag_fc2 = nn.Linear(ndim*2, edim)

        # others
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.5)

    def spec_to_embedding(self, spec):
        # input normalization
        out = spec.unsqueeze(1)
        out = self.spec_bn(out)

        # CNN
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        out = self.layer7(out)
        out = self.layer8(out)
        out = out.squeeze(2)
        out = nn.MaxPool1d(out.size(-1))(out)
        out = out.view(out.size(0), -1)

        # projection
        out = self.song_fc1(out)
        out = self.song_bn(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.song_fc2(out)
        return out

    def text_to_embedding(self, token, mask):
        out = self.bert(token, attention_mask=mask)['last_hidden_state'][:, 0]
        out = self.text_fc1(out)
        out = self.text_bn(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.text_fc2(out)
        return out

    def tag_to_embedding(self, tag):
        out = self.tag_fc1(tag)
        out = self.tag_bn(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.tag_fc2(out)
        return out

    def forward(self, tag, spec, token, mask):
        tag_emb = self.tag_to_embedding(tag)
        song_emb = self.spec_to_embedding(spec)
        text_emb = self.text_to_embedding(token, mask)
        return tag_emb, song_emb, text_emb


class Conv_2d(nn.Module):
    def __init__(self, input_channels, output_channels, shape=3, pooling=2):
        super(Conv_2d, self).__init__()
        self.conv = nn.Conv2d(input_channels, output_channels, shape, padding=shape//2)
        self.bn = nn.BatchNorm2d(output_channels)
        self.relu = nn.ReLU()
        self.mp = nn.MaxPool2d(pooling)

    def forward(self, x):
        out = self.mp(self.relu(self.bn(self.conv(x))))
        return out


class Conv_emb(nn.Module):
    def __init__(self, input_channels, output_channels):
        super(Conv_emb, self).__init__()
        self.conv = nn.Conv2d(input_channels, output_channels, 1)
        self.bn = nn.BatchNorm2d(output_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.relu(self.bn(self.conv(x)))
        return out


class Res_2d(nn.Module):
    def __init__(self, input_channels, output_channels, shape=3, stride=2):
        super(Res_2d, self).__init__()
        # convolution
        self.conv_1 = nn.Conv2d(input_channels, output_channels, shape, stride=stride, padding=shape//2)
        self.bn_1 = nn.BatchNorm2d(output_channels)
        self.conv_2 = nn.Conv2d(output_channels, output_channels, shape, padding=shape//2)
        self.bn_2 = nn.BatchNorm2d(output_channels)

        # residual
        self.diff = False
        if (stride != 1) or (input_channels != output_channels):
            self.conv_3 = nn.Conv2d(input_channels, output_channels, 1, stride=stride, padding=0)
            self.bn_3 = nn.BatchNorm2d(output_channels)
            self.diff = True
        self.relu = nn.ReLU()

    def forward(self, x):
        # convolution
        out = self.bn_2(self.conv_2(self.relu(self.bn_1(self.conv_1(x)))))

        # residual
        if self.diff:
            x = self.bn_3(self.conv_3(x))
        out = x + out
        out = self.relu(out)
        return out


class Res_2d_mp(nn.Module):
    def __init__(self, input_channels, output_channels, pooling=2):
        super(Res_2d_mp, self).__init__()
        self.conv_1 = nn.Conv2d(input_channels, output_channels, 3, padding=1)
        self.bn_1 = nn.BatchNorm2d(output_channels)
        self.conv_2 = nn.Conv2d(output_channels, output_channels, 3, padding=1)
        self.bn_2 = nn.BatchNorm2d(output_channels)
        self.relu = nn.ReLU()
        self.mp = nn.MaxPool2d(pooling)
    def forward(self, x):
        out = self.bn_2(self.conv_2(self.relu(self.bn_1(self.conv_1(x)))))
        out = x + out
        out = self.mp(self.relu(out))
        return out

class SentimentAnalysis:
    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

        S = torch.load('src/sentiment/epoch=2.ckpt', map_location=torch.device('cpu'))['state_dict']
        NS = {k[6:]: S[k] for k in S.keys() if (k[:5] == 'model')}
        ml_alm = MyModel()
        ml_alm.load_state_dict(NS)
        self.ml_alm = ml_alm.eval()

        self.word_to_vec = pickle.load(open('src/sentiment/w2v.pkl', 'rb'))

        alm_moods = ['anger', 'fearful', 'happy', 'sad', 'surprised']
        audioset_moods = ['angry', 'exciting', 'funny', 'happy', 'sad', 'scary', 'tender']
        self.concat_moods = list(set(['text_' + m for m in alm_moods] + ['music_' + m for m in audioset_moods]))
        self.concat_moods.sort()
        with torch.no_grad():
            self.mood_embs = ml_alm.tag_to_embedding(torch.tensor([self.word_to_vec[mood.split('_')[1]] for mood in self.concat_moods]))

    def __text_to_emb(self, text):
        tokens = self.tokenizer([text, text], return_tensors='pt', padding=True, truncation=True) # made a list of the text to avoid batch_normalization issue
        with torch.no_grad():
            emb = self.ml_alm.text_to_embedding(tokens['input_ids'], tokens['attention_mask'])[0].detach().cpu().unsqueeze(0)
        return emb

    def textAnalysis(self, content):
        emb = self.__text_to_emb(content)
        sim = metrics.pairwise.cosine_similarity(self.mood_embs[-5:], emb)
        text_moods = [i.split('_')[1] for i in self.concat_moods[-5:]]
        text_sim = text_moods[sim.argmax()]
        return text_sim
    
