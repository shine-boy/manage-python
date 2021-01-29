
# import pathlib
#
# import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import pymongo
import io
# import seaborn as sns
#
import tensorflow as tf
#
# from tensorflow import keras
# from tensorflow.keras import layers

myclient = pymongo.MongoClient("mongodb://192.168.128.146:27018")
mydb = myclient['pledge']
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


def find(lis, target):
    try:
        lis.index(target)
        return True
    except ValueError as v:
        return False


def findIndex(lis, target):
    index = -1
    try:
        index = lis.index(target)
    except ValueError as v:
        return index
    return index


# 划分各类别数据，并得到分类列表
def divide_type(label, types=[]):
    alldata = []
    data = []
    if os.path.exists('./types.txt') is False:
        with open('./types.txt', 'w') as f:
            f.close()
    with open('./types.txt', 'r') as f:
        alldata = f.readlines()
        f.close()
    with open('./types.txt', 'w') as f:
        labels = []
        if len(alldata) > 0:
            labels = alldata[0][:-1].split("\t")
        else:
            alldata.append(labels)
        index = findIndex(labels, label) + 1
        print(index)

        if index > 0:
            data = alldata[index][:-1].split("\t")
        else:
            labels.append(label)
        alldata[0] = '\t'.join(labels) + '\n'
        for type in types:
            if find(data, type) is False:
                data.append(type)
        if index > 0:
            alldata[index] = '\t'.join(data) + '\n'
        else:
            alldata.append('\t'.join(data) + '\n')

        f.writelines(alldata)
        # numpy.fromfile('./types',sep=' ')
        f.close()
    return data


# 归一
def to_one(label, dataFrame):
    column = dataFrame[label].copy()
    types = divide_type(label, column.unique())
    print(types)
    for i in range(column.size):
        column.loc[i] = findIndex(types, column[i])
    dataFrame[label] = column
    return column
    print(column)
def getData():
    column_names =  ["city", 'openTime', 'region', 'province', 'address', 'decoration', 'houseType', 'volumeRatio',
            'greenRate', 'proYears', 'planHouse', 'parkRatio', 'towards', 'proComp', 'developer', 'apartment',
            'buildType','source','secondOrNew','buildArea','avgPrice']

    raw_dataset = pd.read_csv('../data/house.csv', names=column_names,low_memory=False,
                              na_values="?", comment='\t',
                               skipinitialspace=True)
    dataset = raw_dataset.copy()

    print(dataset.isna().sum())
if __name__ == '__main__':
    getData()
    pass