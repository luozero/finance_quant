import sys
import os
sys.path.append(r'../../')
from stock_deeplearning.training.data_loader import StockLoader as SL

import torch
# import torchvision
# import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Para:
  def __init__(self):
    self.num0 = 8
    self.num1 = 4
    self.num2 = 2
    self.num3 = 1
    # self.num4 = 9
    # self.num5 = 6
    # self.num6 = 3
    # self.num7 = 2
para = Para()

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.fc1 = nn.Linear(para.num0, 1)
    self.fc2 = nn.Linear(para.num1, para.num2)
    self.fc3 = nn.Linear(para.num2, para.num3)
    # self.fc4 = nn.Linear(para.num3, para.num4)
    # self.fc5 = nn.Linear(para.num4, para.num5)
    # self.fc6 = nn.Linear(para.num5, para.num6)
    # self.fc7 = nn.Linear(para.num6, para.num7)
    # self.fc8 = nn.Linear(para.num5, 5)

  def forward(self, x):
    x = (self.fc1(x))
    # x = F.relu(self.fc2(x))
    # x = F.relu(self.fc3(x))
    # x = F.relu(self.fc4(x))
    # x = F.relu(self.fc5(x))
    # # x = F.relu(self.fc6(x))
    # # x = F.relu(self.fc7(x))
    # x = self.fc3(x)
    return x

def training():

  criterion = nn.MSELoss()
  optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

  trainloader = stock_loader.train_loader()

  for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
      # get the inputs; data is a list of [train_inputs, train_output]
      train_inputs, train_output = data

      # zero the parameter gradients
      optimizer.zero_grad()

      # forward + backward + optimize
      output = net(train_inputs)
      loss = criterion(output, train_output)
      print("index:", i, "train_output", train_output, "output", output)
      loss.backward()
      optimizer.step()

      # print statistics
      running_loss += loss.item()
      if i % 20 == 19:    # print every 2000 mini-batches
        print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 20))
        running_loss = 0.0

  print('Finished Training!')
  torch.save(net.state_dict(), PATH)

# net = torch.load(PATH)
def inferencing():
  correct = 0
  total = 0
  testloader = stock_loader.test_loader()
  with torch.no_grad():
    for data in testloader:
      test_inputs, test_output = data
      output = net(test_inputs)
      total += 1

      correct += torch.abs(test_output - output) / torch.abs(output)
      print("test_output", test_output, "output", output)
      # print("total", total, "correct", correct)

  # print('Accuracy of the network on the ', total, 'test inputs: %d %%' % (
  #     100 * correct / total))

# ADX	ADXR	APO	aroondown	aroonup	AROONOSC	BOP	CCI	CMO	DX	MACD	MFI	PPO	ROCP	RSI	STOCHslowk	STOCHslowd	STOCHRSIfastk	STOCHRSIfastd	TRIX	TRIX
# ["1day", "2day","3day","4day","5day"]
PATH = '../../data/momentum_net.pth'
stock_loader = SL("test", "../../data/talib_factor", 0.9, ["1day"], ["ADX", "ADXR", "APO", "aroondown", "RSI", "MACD", "STOCHRSIfastk", "BOP"])
net = Net()
training()
inferencing()

