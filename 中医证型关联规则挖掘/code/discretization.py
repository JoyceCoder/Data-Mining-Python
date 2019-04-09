#-*- coding: utf-8 -*-
'''
聚类离散化，最后的result的格式为：
      1           2           3           4
A     0    0.178698    0.257724    0.351843
An  240  356.000000  281.000000   53.000000
即(0, 0.178698]有240个，(0.178698, 0.257724]有356个，依此类推。
'''
from __future__ import print_function
import pandas as pd
from sklearn.cluster import KMeans #导入K均值聚类算法

datafile = '../data/data.xls' #待聚类的数据文件
processedfile = '../tmp/data_processed.xls' #数据处理后文件
"""
outfile = '../tmp/data_discret.xls' #离散化后的数据

data = pd.read_excel(datafile)
result = pd.read_excel(processedfile)

df = data[['肝气郁结证型系数', '热毒蕴结证型系数', '冲任失调证型系数', '气血两虚证型系数', '脾胃虚弱证型系数', '肝肾阴虚证型系数']].copy()
df.columns = ['A','B','C','D','E','F']

df.loc[(df.A>result.iloc[0,0])&(df.A<result.iloc[0,1]),'Ax']= 'A1'
df.loc[(df.A>result.iloc[0,1])&(df.A<result.iloc[0,2]),'Ax'] = 'A2'
df.loc[(df.A>result.iloc[0,2])&(df.A<result.iloc[0,3]),'Ax'] = 'A3'
df.loc[(df.A>result.iloc[0,3]),'Ax']= 'A4'

df.loc[(df.B>result.iloc[2,0])&(df.B<result.iloc[2,1]),'Bx']= 'B1'
df.loc[(df.B>result.iloc[2,1])&(df.B<result.iloc[2,2]),'Bx'] = 'B2'
df.loc[(df.B>result.iloc[2,2])&(df.B<result.iloc[2,3]),'Bx'] = 'B3'
df.loc[(df.B>result.iloc[2,3]),'Bx']= 'B4'

df.loc[(df.C>result.iloc[4,0])&(df.C<result.iloc[4,1]),'Cx']= 'C1'
df.loc[(df.C>result.iloc[4,1])&(df.C<result.iloc[4,2]),'Cx'] = 'C2'
df.loc[(df.C>result.iloc[4,2])&(df.C<result.iloc[4,3]),'Cx'] = 'C3'
df.loc[(df.C>result.iloc[4,3]),'Cx']= 'C4'

df.loc[(df.D>result.iloc[6,0])&(df.D<result.iloc[6,1]),'Dx']= 'D1'
df.loc[(df.D>result.iloc[6,1])&(df.D<result.iloc[6,2]),'Dx'] = 'D2'
df.loc[(df.D>result.iloc[6,2])&(df.D<result.iloc[6,3]),'Dx'] = 'D3'
df.loc[(df.D>result.iloc[6,3]),'Dx']= 'D4'

df.loc[(df.E>result.iloc[8,0])&(df.E<result.iloc[8,1]),'Ex']= 'E1'
df.loc[(df.E>result.iloc[8,1])&(df.E<result.iloc[8,2]),'Ex'] = 'E2'
df.loc[(df.E>result.iloc[8,2])&(df.E<result.iloc[8,3]),'Ex'] = 'E3'
df.loc[(df.E>result.iloc[8,3]),'Ex']= 'E4'

df.loc[(df.F>result.iloc[10,0])&(df.F<result.iloc[10,1]),'Fx']= 'F1'
df.loc[(df.F>result.iloc[10,1])&(df.F<result.iloc[10,2]),'Fx'] = 'F2'
df.loc[(df.F>result.iloc[10,2])&(df.F<result.iloc[10,3]),'Fx'] = 'F3'
df.loc[(df.F>result.iloc[10,3]),'Fx']= 'F4'



df.to_excel(outfile)

"""
typelabel ={u'肝气郁结证型系数':'A', u'热毒蕴结证型系数':'B', u'冲任失调证型系数':'C', u'气血两虚证型系数':'D', u'脾胃虚弱证型系数':'E', u'肝肾阴虚证型系数':'F'}
k = 4 #需要进行的聚类类别数

#读取数据并进行聚类分析
data = pd.read_excel(datafile) #读取数据
keys = list(typelabel.keys())
result = pd.DataFrame()

if __name__ == '__main__': #判断是否主窗口运行，这句代码的作用比较神奇，有兴趣了解的读取请自行搜索相关材料。
  for i in range(len(keys)):
    #调用k-means算法，进行聚类离散化
    print(u'正在进行“%s”的聚类...' % keys[i])
    kmodel = KMeans(n_clusters = k, n_jobs = 1) #n_jobs是并行数，一般等于CPU数较好
    kmodel.fit(data[[keys[i]]].as_matrix()) #训练模型
    
    r1 = pd.DataFrame(kmodel.cluster_centers_, columns = [typelabel[keys[i]]]) #聚类中心
    #print(r1.columns,r1.values)
    r2 = pd.Series(kmodel.labels_).value_counts() #分类统计
    r2 = pd.DataFrame(r2, columns = [typelabel[keys[i]]+'n']) #转为DataFrame，记录各个类别的数目
    #print(r2.columns,r2.values)
    #r = pd.concat([r1, r2], axis = 1).sort(typelabel[keys[i]]) #匹配聚类中心和类别数目
    r = pd.concat([r1, r2], axis = 1).sort_values(typelabel[keys[i]])
    #print(r.columns,r.values)
    r.index = [1, 2, 3, 4]
    
    #r[typelabel[keys[i]]] = pd.rolling_mean(r[typelabel[keys[i]]], 2) #rolling_mean()用来计算相邻2列的均值，以此作为边界点。
    r[typelabel[keys[i]]] = r[typelabel[keys[i]]].rolling(2).mean()
    r[typelabel[keys[i]]][1] = 0.0 #这两句代码将原来的聚类中心改为边界点。 
    result = result.append(r.T)

  #result = result.sort() #以Index排序，即以A,B,C,D,E,F顺序排
  result = result.sort_values(by = list(result.index),axis=1) #以Index排序，即以A,B,C,D,E,F顺序排
  result.to_excel(processedfile)


  