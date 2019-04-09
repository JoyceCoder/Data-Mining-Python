#-*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd

#找出频繁项集
#使用频繁项集生成候选集
"""
找出频繁项集，寻找关联规则
d：data dataframe
support：设定的最小支持度
confidence: 设定的最小可信度
ms: 字母分隔符
"""
def find_rule(d,support,confidence,ms='--'):#默认分割符为--
#找出频繁集
    
result = pd.DataFrame(index=['support','confidence'])

support_series = 1.0*d.sum()/len(d)
#筛选符合支持度的项集
columns = list(support_series[support_series > support].index)

k=0 #起始频繁项集个数

#寻找关联规则，直到频繁项集为空
while len(columns) > 1:
    k = k+1 #初始为单元素L1->C1
    print(u'\n正在搜索元素个数为%s的频繁项集...' %k)

    column = GeneratorCk(column,ms)
    #返回的是含有k+1个元素的频繁项集

    #重新计算支持度
    sf = lambda i:d[i].prod(axis=1,numeric_only=True)#只对数字按行相乘
    d2 = pd.DataFrame(list(map(sf,column)), index = [ms.join(i) for i in column]).T #转置为了计算每个规则的数量
    
    #筛选
    support_series_2 = 1.0*d2[ms.join(i) for i in column]].sum()/len(d)
    column = list(support_series_2[support_series_2 > support].index)

    support_series = support_series.append(support_series_2)

    column2 = []
    #寻找关联规则
    for i in column:
        i = i.split(ms)
        for j in range(len(i)):
            column2.append(i[:j]+i[j+1:]+j[j:j+1]) #0:1 + 2:-1 1

    confidence_series = pd.Series(index=[ms.join(i) for i in column2])

    #计算可信度
    for i in column2:
        confidence_series[ms.join(i)] = support_series[ms.join(sorted(i))]/support_series[ms.join(i[:len(i)-1])]

    #筛选Lk
    for i in confidence_series[confidence_series > confidence].index:
        result[i] = 0.0
        result[i]['confidence'] = confidence_series[i]
        result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]
    
    #对结果sort
    result = result.T.sort_index()

    print('result:')
    print(result)

    return result

def GeneratorCk(column,ms):
    #对元素分割后重排
    x = list(map(lambda i:sorted(i.split(ms)),column))
    l = len(x[0])

    r = []
    for i in range(len(x)):
        for j in (i,range(len(x))):
            #避免重复操作
            if (x[i][:l-1] == x[j][:l-1]) &(x[i][l-1]!=x[j][l-1]):
                r.append(x[i][:l-1]+sorted(x[i][l-1],x[j][l-1]))
    return r