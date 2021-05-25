# coding='utf-8'
import math
import copy
import numpy as np

# 数据初始化
labels_word = ['色泽','根蒂','敲声','纹理','脐部','触感','密度','含糖率']
dataSet = [
    ['青绿','蜷缩','浊响','清晰','凹陷','硬滑',0.697,0.460,'好瓜'],
    ['乌黑','蜷缩','沉闷','清晰','凹陷','硬滑',0.774,0.376,'好瓜'],
    ['乌黑','蜷缩','浊响','清晰','凹陷','硬滑',0.634,0.264,'好瓜'],
    ['青绿','蜷缩','沉闷','清晰','凹陷','硬滑',0.608,0.318,'好瓜'],
    ['浅白','蜷缩','浊响','清晰','凹陷','硬滑',0.556,0.215,'好瓜'],
    ['青绿','稍蜷','浊响','清晰','稍凹','软粘',0.403,0.237,'好瓜'],
    ['乌黑','稍蜷','浊响','稍糊','稍凹','软粘',0.481,0.149,'好瓜'],
    ['乌黑','稍蜷','浊响','清晰','稍凹','硬滑',0.437,0.211,'好瓜'],
    ['乌黑','稍蜷','沉闷','稍糊','稍凹','硬滑',0.666,0.091,'坏瓜'],
    ['青绿','硬挺','清脆','清晰','平坦','软粘',0.243,0.267,'坏瓜'],
    ['浅白','硬挺','清脆','模糊','平坦','硬滑',0.245,0.057,'坏瓜'],
    ['浅白','蜷缩','浊响','模糊','平坦','软粘',0.343,0.099,'坏瓜'],
    ['青绿','稍蜷','浊响','稍糊','凹陷','硬滑',0.639,0.161,'坏瓜'],
    ['浅白','稍蜷','沉闷','稍糊','凹陷','硬滑',0.657,0.198,'坏瓜'],
    ['乌黑','稍蜷','浊响','清晰','稍凹','软粘',0.360,0.370,'坏瓜'],
    ['浅白','蜷缩','浊响','模糊','平坦','硬滑',0.593,0.042,'坏瓜'],
   [ '青绿','蜷缩','沉闷','稍糊','稍凹','硬滑',0.719,0.103,'坏瓜']  
]

# 需要判断的个体
value = ['青绿','蜷缩','浊响','清晰','凹陷','硬滑',0.697,0.460,'好瓜']

# 用到的函数
''' 
统计列表中元素种类和个数
    input:dataSet中某一列,数据类型为列表
    output:字典
'''
def num_value(items):
    count = {}
    for item in items:
        count[item] = count.get(item, 0) + 1
    return count

''' 
根据好瓜和坏瓜分割数据集,
    input: dataSet
    output: 字典,{'好瓜':[],'坏瓜':[]}
'''
def splite_data(dataSet,count_pc):
    x = {}
    for i in count_pc:
        x[i] = []
        for j in dataSet:    
            if j[-1] == i:
                x[i].append(j)          
    return x

# 计算先验概率
x = [i[-1] for i in dataSet]
count_pc = num_value(x)
Pc = {}
for i in count_pc:
    Pc[i] = (count_pc[i]+1)/(len(x)+len(count_pc))

# 分割数据集
data_block = splite_data(dataSet,count_pc)

# 计算条件概率
Px_c = []
for i in range(len(labels_word)): # 第i个属性
    Pi = {}
    if isinstance(value[i], str): # 离散和连续元素分开处理
        X = [item[i] for item in dataSet]
        Count = num_value(X)

        for j in data_block: # 两次循环：好瓜和坏瓜,分别计算条件概率
            xx = [item[i] for item in data_block[j]]
            count = num_value(xx)

            Pi[value[i] + '|' + j] = (count[value[i]]+1)/(len(data_block[j])+len(Count))
        Px_c.append(copy.deepcopy(Pi))    

    elif isinstance(value[i], float):
        for j in data_block:
            xx = np.array([item[i] for item in data_block[j]],dtype=float)
            uc = np.sum(xx)/np.shape(xx)[0]
            sigma = math.sqrt(np.sum((xx-uc)*(xx-uc))/np.shape(xx)[0])

            Pi[labels_word[i]+':'+str(value[i]) + '|' + j] = (1/(math.sqrt(2*math.pi)*sigma))*math.exp(-1*((value[i]-uc)**2)/(2*sigma**2))
        Px_c.append(copy.deepcopy(Pi)) 


# 计算最终概率
P = {}
for i in data_block: # 好瓜 和 坏瓜
    P[i] = Pc[i]
    for j in range(len(labels_word)):
        if isinstance(value[j], str):
            P[i] = P[i] * Px_c[j][value[j] + '|' + i]
        elif isinstance(value[j], float):
            P[i] = P[i] * Px_c[j][labels_word[j]+':'+str(value[j]) + '|' + i] 


# 寻找最大概率并判断标签
pmax = 0
label = ''
for i in P:
    if pmax < P[i]:
        pmax = P[i]
        label = i

print(P)
print('该测试元素为:'+label)

