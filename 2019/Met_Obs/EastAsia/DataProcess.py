import pandas as pd
import numpy as np
import os, datetime

pwd = os.getcwd()

ssList = {'首爾':'471080', '濟州':'471840', 
          '東京':'476620', '那霸機場':'479360',
          '北京':'545110', '上海':'583620', '福州':'588470', '廈門':'591340'}
vars = ['T2', 'WS', 'WD']

start = '2019-01-01-00'
end = '2019-12-31-23'
Times = pd.date_range(start, end, freq='1d').strftime('%Y-%m-%d')

for var in vars:
    Data = pd.DataFrame(index=pd.date_range(start, end, freq='1h'))
    for st in ssList:

        inFil = os.path.join(pwd, 'data_in', ssList[st]+'99999.csv')
        data = pd.read_csv(inFil, encoding='big5', index_col=1)
        data = data.loc[data['REPORT_TYPE']=='FM-12']


        if (var=='T2'):
           df = pd.Series(data['TMP'].str.split(',', 2, True)[0], name='T2').astype(int)/10
        elif (var=='WS'):
           df = pd.Series(data['WND'].str.split(',', 5, True)[3], name='WS').astype(int)/10
        elif (var=='WD'):
           df = pd.Series(data['WND'].str.split(',', 5, True)[0], name='WD').astype(int)

        df.index = [datetime.datetime.strptime(tt, '%Y-%m-%dT%H:%M:%S') for tt in df.index]
        Data = pd.concat([Data, df], axis=1)

    Data.index = pd.to_datetime(Data.index)
    Data.columns = ssList
    Data = Data.replace([999.9, 999, np.nan], -999)

    print(max(Data))

    outDir = os.path.join(pwd, 'data_out', var)
    for dd in Times:
        print(dd)
        outData = Data.loc[dd]
        outData.index = [datetime.datetime.strftime(dd, '%Y-%m-%d-%H') for dd in outData.index]
        outFil = os.path.join(outDir, dd + '_' + var + '_obs.csv')
        outData.to_csv(outFil, encoding='utf-8-sig')
        print(outData)
