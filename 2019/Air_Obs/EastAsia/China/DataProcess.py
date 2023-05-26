import pandas as pd
import datetime
import calendar
import os


pwd = os.getcwd()
dataDir = os.path.join(pwd, 'RawData')
outDir  = os.path.join(pwd, 'ChinaData')

stons = ['北京', '上海', '福州', '廈門']
vars = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'NMHC']
Time = pd.date_range('20190101', '20191231', freq='1d').strftime('%Y%m%d')

def Utrans(var, df):
    if (var=='SO2'):
       df = round(df*0.382, 2)
    elif (var=='NO2'):
       df = round(df*0.531, 2)
    elif (var=='O3'):
       df = round(df*0.509, 2)
    else:
       df = round(df*1, 2)
    return df

for var in vars:
    print(var)
    if (var == 'NMHC'):
       pass
    else:
       Data = pd.DataFrame()
       for tt in Time:
           try:
              data= pd.read_csv(dataDir + '/china_cities_' + tt + '.csv', index_col=0, encoding='utf-8-sig')
              data.index = (data.index.map(str) + data['hour'].map(str))

              stData = pd.DataFrame()
              for st in stons:
                 df = data.loc[data['type']==var][st]
                 df.index = [datetime.datetime.strptime(dd, '%Y%m%d%H')\
                            .strftime('%Y-%m-%d-%H') for dd in df.index]
                 stdf = pd.Series(data=Utrans(var, df), name=st, index=df.index)
                 stData = pd.concat([stData, stdf], axis=1, sort=False)
           except FileNotFoundError:
               stData = pd.DataFrame(columns=stons,
                                     index=pd.date_range(tt, freq='1h', periods=24))
               stData.index = [tt.strftime('%Y-%m-%d-%H') for tt in stData.index]
           Data = pd.concat([Data, stData], axis=0, sort=False)
       print(Data)
       Data = Data.fillna(-999)
       outFile = os.path.join(outDir, 'China_' + var + '.csv')
       Data.to_csv(outFile, encoding='utf-8-sig')


