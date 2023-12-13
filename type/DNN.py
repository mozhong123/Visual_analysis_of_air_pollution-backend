# encoding=utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import json
import os
import csv
import glob
import pandas as pd

# DNN模型
class DnnNet(nn.Module):
    def __init__(self):
        super(DnnNet,self).__init__()
        self.l1 = nn.Linear(5, 50)
        self.l2 = nn.Linear(50, 30)
        self.l3 = nn.Linear(30, 11)
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = self.dropout(x)
        x = F.relu(self.l2(x))

        return self.l3(x)

# input = [[day1, month1, year1, lat1, lon1], [day2, month2, year2, lat2, lon2]......]
# 例如input = [[1, 1, 2018, 18.34, 109.25], [30, 11, 2020, 11.34, 102.25]]
def predict(input):
    dataset = np.array(input).astype(np.float32)
    # 进行放缩
    max_min = np.load('max_min.npz')
    max_data = max_min['max'][:5]
    min_data = max_min['min'][:5]
    dataset = torch.tensor((dataset-min_data)/(max_data-min_data))
    # 预测
    # 加载模型
    model = DnnNet()
    model.load_state_dict(torch.load('dnn_model.pth'))
    output = None
    with torch.no_grad():
        model.eval()
        output = model(dataset)
        output = np.clip(output, 0, 1)

    # 对output进行还原
    max_output = max_min['max'][5:]
    min_output = max_min['min'][5:]
    output = output * (max_output - min_output) + min_output
    #print(output)
    return output

# predict([[1, 1, 2018, 18.34, 109.25], [30, 11, 2020, 11.34, 102.25]])