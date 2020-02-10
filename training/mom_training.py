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
    self.first_num = 21
    self.second_num = 8
    self.third_num = 4
    self.forth_num = 2
para = Para()

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.fc1 = nn.Linear(para.first_num, para.second_num)
    self.fc2 = nn.Linear(para.second_num, para.third_num)
    self.fc3 = nn.Linear(para.third_num, para.forth_num)
    self.fc4 = nn.Linear(para.forth_num, 1)

  def forward(self, x):
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = F.relu(self.fc3(x))
    x = self.fc4(x)
    return x

def training():

  criterion = nn.SmoothL1Loss()
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
      loss = criterion(output, torch.Tensor([train_output]))
      loss.backward()
      optimizer.step()

      # print statistics
      running_loss += loss.item()
      if i % 20 == 19:    # print every 2000 mini-batches
        print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 20))
        running_loss = 0.0

  print('Finished Training')
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
      correct += (test_output - output) / output
      print("total", total, "correct", correct)

  print('Accuracy of the network on the ', total, 'test inputs: %d %%' % (
      100 * correct / total))

PATH = '../../data/momentum_net.pth'
stock_loader = SL("000001.XSHE", "../../data/talib_factor", 0.9, "5day")
net = Net()
training()
inferencing()

