import pandas as pd
import os

pwd = os.getcwd()
Conts = ['Korea', 'Japan', 'China']
vars = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3', 'NMHC']

Time = pd.date_range('2019-01-01-00', '2019-12-31-23', freq='1h')\
                     .strftime('%Y-%m-%d-%H')
KNMHC = pd.DataFrame(-999, index=Time, columns=['首爾', '濟州'])
CNMHC = pd.DataFrame(-999, index=Time, columns=['北京', '上海', '福州', '廈門'])

JNAN = pd.DataFrame(-999, index=Time, columns=['東京', '沖繩'])


for var in vars:
   Data = pd.DataFrame()
   for Cont in Conts:
      try:
         inFil = os.path.join(pwd, Cont, Cont+'Data', Cont + '_' + var + '.csv')
         df = pd.read_csv(inFil, encoding='utf-8-sig', index_col=0)
      except FileNotFoundError:
         if (Cont=='Korea'):
            df = KNMHC
         elif (Cont=='China'):
            df = CNMHC
         elif (Cont=='Japan'):
            df = JNAN
      Data = pd.concat([Data, df], axis=1)
   Data = Data.fillna(-999)
   print(Data)
   

   outFil = os.path.join(pwd, 'data_out', '2019' + var + '_PerHour.csv')
   Data.to_csv(outFil, encoding='utf-8-sig')

