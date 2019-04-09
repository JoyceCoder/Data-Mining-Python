import pandas as pd

datafile = '../tmp/data_stipu.csv'
standrandfile = '../tmp/data_stand.csv'

data = pd.read_csv(datafile)

#数据变换
df = data[['LAST_TO_END','FLIGHT_COUNT','SEG_KM_SUM','avg_discount']].copy()#数据副本的复制
df['L'] = (pd.to_datetime(data['LOAD_TIME']) - pd.to_datetime(data['FFP_DATE'])).dt.days/30#计算日期差,单位为月
df.rename(columns={'LAST_TO_END':'R','FLIGHT_COUNT':'F','SEG_KM_SUM':'M','avg_discount':'C'},inplace = True)#列名重命名

#数据标准化
df = (df - df.mean(axis=0))/(df.std(axis=0))#均值标准化
df.columns = ['z'+i for i in df.columns]#对数据列名重命名

df.to_csv(standrandfile)