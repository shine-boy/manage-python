
# import pathlib
#
# import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import pymongo
import io
import seaborn as sns
#
# import tensorflow as tf
# #
# from tensorflow import keras
# from tensorflow.keras import layers

myclient = pymongo.MongoClient("mongodb://192.168.142.1:27017")
mydb = myclient['dongfangcaifu']
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


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

def getStockData():
    names=mydb['names'].find({})
    # names=list(ns)
    result=[]
    def isNext(current,next):
        t=next.timestamp()-current.timestamp()
        if t>110 and t<130:
            return True
        return False

    for name in names:
        code=name['code']
        item=mydb[code].find({},{'_id':0}).sort([('time',1)])
        current=item.next()
        for next in item:
            if isNext(current['time'],next['time']):
                current['next2']=next['f43']
                result.append(current)
            current=next
    data=pd.DataFrame(result)
    data.to_csv("../data/stock.csv",index=False)
    # print(data.head())

        # print(list(item))

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
    raw_dataset = pd.read_csv('../data/stock.csv',  low_memory=False,
                              na_values="?", comment='\t',index_col=[0],
                              skipinitialspace=True)
    dataset = raw_dataset.copy()
    dataset.pop('time')
    print(dataset.size)
    dataset=dataset[~dataset.isin([str('-')])]
    print(dataset.size)
    # dataset.pop("f58")
    # to_one('f127', dataset)
    # to_one('f128', dataset)
    # code=dataset['f57']
    # code=map(lambda x:int(x),code)
    # dataset['f57']=list(code)
    # dataset.to_csv("../data/stock.csv")
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_labels = train_dataset.pop('next2')
    test_labels = test_dataset.pop('next2')

    train_dataset = train_dataset.astype(float)
    train_stats = train_dataset.describe()
    # 转置
    train_stats = train_stats.transpose()
    print(train_stats)
    print(train_dataset.keys())
    # 数据规范化，归一化
    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    pass