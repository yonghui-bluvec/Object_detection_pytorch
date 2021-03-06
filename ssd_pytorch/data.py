import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import numpy as np


class Mydataset(Dataset):
    def __init__(self, txt_path, transform):
        super(Dataset).__init__()
        input = open(txt_path, "r")
        lines = input.readlines()
        input.close()
        data = []
        self.maxbnum = 0
        for line in lines:
            line = line.strip()
            path = line.split()[0]
            labels = convert_label(line.split()[1:])
            if len(labels) > self.maxbnum:
                self.maxbnum = len(labels)
            data.append([path, labels])
        self.data = data
        self.transform = transform

    def __getitem__(self, index):
        path, labels = self.data[index]
        image =  Image.open(path)
        #image = cv2.imread(path)
        image = self.transform(image)
        for i in range(self.maxbnum - len(labels)):
            labels.append([-1, -1, -1, -1, -1])
        labels = torch.Tensor(np.array(labels))
        return image, labels
    def __len__(self):
        return len(self.data)

def ssd_transform():
    transform = transforms.Compose([
                                    transforms.Resize((300,300)),
                                    transforms.ToTensor(),
                                    ])
    return transform

def convert_label(labels):
    output = []
    for label in labels:
        xmin, ymin, xmax, ymax , cla = label.split(",")
        output.append([float(xmin), float(ymin), float(xmax), float(ymax) , int(cla)])
    return output