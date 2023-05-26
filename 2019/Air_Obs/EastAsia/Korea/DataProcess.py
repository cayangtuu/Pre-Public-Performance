import pandas as pd
import numpy as np
import os, datetime
from findst import Korea_ID

pwd = os.getcwd()
stidFil = os.path.join(pwd, 'RawData', '韓國空品站位置(首爾與濟州).xlsx')
stons = Korea_ID(stidFil)

vars = ['PM25', 'PM10', 'SO2', 'NO2', 'O3']
Month = pd.date_range('2019-01', periods=12, freq='M').strftime('%Y-%m-%d')

def Utrans(var, df):
    if (var=='SO2' or var=='NO2' or var=='O3'):
       df = df*1000
    else:
       df = df*1
    return df

for var in vars:
    KData = pd.DataFrame()
    for ston in stons:
        Data = pd.DataFrame()
        for mm in Month:
            dataFil = os.path.join(pwd, 'RawData', mm[:7] + '_Korea_AQ.xlsx')
            data = pd.read_excel(dataFil, usecols=['측정소코드','측정일시',var])
            data.columns = ['id', 'date', var]
            stdf = pd.DataFrame()
            for st in stons[ston]:
                df = pd.Series(data=data.loc[data['id']==st][var], name=st)
                df = Utrans(var, df)
                df.column = st
                df.index = pd.date_range(mm[:7], mm+'-23', freq='1h') \
                                         .strftime('%Y-%m-%d-%H')
                stdf = pd.concat([stdf, df], axis=1, sort=False)
            Data = pd.concat([Data, stdf], axis=0, sort=False)
        Data['avg'] = round(Data.mean(axis=1),2)

        KData = pd.concat([KData, Data['avg']], axis=1, sort=False)
    KData.columns = stons.keys()
    KData = KData.fillna(-999)
    print(KData)

    if (var == 'PM25'):
       var = 'PM2.5'
    outFil = os.path.join(pwd, 'KoreaData', 'Korea_' + var + '.csv')
    KData.to_csv(outFil, encoding='utf-8-sig')


