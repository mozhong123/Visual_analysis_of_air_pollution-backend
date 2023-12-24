#!/usr/bin/env python
#-*-coding:utf-8-*-
#@File:lstm.py


from torch.autograd import Variable
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
import psycopg2
import json


class RNN(nn.Module):
    def __init__(self, input_size):
        super(RNN, self).__init__()
        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=5,
            num_layers=3,
            batch_first=True
        )
        self.out = nn.Sequential(
            nn.Linear(5, 1)
        )

    def forward(self, x):
        r_out, (h_n, h_c) = self.rnn(x, None)  # None 表示 hidden state 会用全0的 state
        out = self.out(r_out)
        return out


class TrainSet():
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __getitem__(self, index):
        return self.data[index], self.label[index]

    def __len__(self):
        return len(self.data)


def getData(city='上海市'):
    conn = psycopg2.connect(database="可视化", user="postgres", password="123", host="127.0.0.1",port="5432")  ##根据自己的数据库修改
    cursor = conn.cursor()

    command = "select pm2_5,date from data_city where city='%s' order by date DESC ;"%city
    cursor.execute(command)
    tuples = cursor.fetchall()
    return tuples

tuples=getData()

Y=[]
X=[]
for i in range(len(tuples)):
    Y.append(tuples[i][0])
    X.append(i)

#print(Y)
test_y=Y[-100:]
test_x=X[-100:]

X=X[:-100]
Y=Y[:-100]

X2=[]
for i in range(len(Y)-5):
    data_pas=[]
    for j in range(5):
        data_pas.append(Y[i+j])
    X2.append(data_pas)
###########################################
test_x2=[]
for i in range(len(test_y)-5):
    data_pas=[]
    for j in range(5):
        data_pas.append(test_y[i+j])
    test_x2.append(data_pas)
test_y2=test_y[5:]
test_xx=Variable(torch.FloatTensor(test_x2))#得到一个批次中的特征属性数据
test_yy=Variable(torch.FloatTensor(test_y2))#得到一个批次中的特征属性数据
trainset = TrainSet(test_xx,test_yy)
loader_test=DataLoader(trainset, batch_size=16,shuffle=False)
##########################################
Y2=Y[5:]
#print(Y2)
xx=Variable(torch.FloatTensor(X2))#得到一个批次中的特征属性数据
yy=Variable(torch.FloatTensor(Y2))#得到一个批次中的特征属性数据
trainset = TrainSet(xx,yy)
loader=DataLoader(trainset, batch_size=32,shuffle=False)

def train(n = 5,LR = 0.001,EPOCH = 500,train_end = -500):
    rnn = RNN(n)
    optimizer = torch.optim.Adam(rnn.parameters(), lr=LR)  # optimize all cnn parameters
    loss_func = nn.MSELoss()

    for step in range(EPOCH):
        for x, y in loader:
            # print( torch.unsqueeze(xx[k], dim=0))
            output = rnn(torch.unsqueeze(x, dim=0))
            loss = loss_func(torch.squeeze(output), y)
            optimizer.zero_grad()  # clear gradients for this training step
            loss.backward()  # back propagation, compute gradients
            optimizer.step()
        if step % 10 == 0:
            print(step, loss)
            torch.save(rnn, 'rnn.pkl')
    torch.save(rnn, 'rnn.pkl')


    prediction = []

    for tx, ty in loader_test:
        # print(tx)
        output = rnn(torch.unsqueeze(tx, dim=0))
        for tmp in output.detach().numpy():
            for tmp1 in tmp:
                prediction.append(tmp1.tolist()[0])

    # print(prediction)

    plt.figure(figsize=(20, 7))  # 设定绘图窗口大小
    xplot = plt.plot(test_x, test_y, 'o')  # 绘制原始数据
    yplot = plt.plot(test_x[5:], prediction, "o")  # 绘制拟合数据
    plt.xlabel('X')  # 更改坐标轴标注
    plt.ylabel('Y')  # 更改坐标轴标注
    #plt.legend([xplot, yplot], ['Data', 'Prediction under 2000 epochs'])  # 绘制图例
    plt.show()

train()
