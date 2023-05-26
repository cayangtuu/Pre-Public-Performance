import pandas as pd
import numpy as np
import datetime
import calendar
import os


pwd = os.getcwd()

stons = {'北部空品區':  ['基隆', '汐止', '萬里', '新店', '土城', '板橋', 
                         '新莊', '菜寮', '林口', '淡水', '士林', '中山', 
                         '萬華', '古亭', '松山', '桃園', '大園', '觀音',
                         '平鎮', '龍潭', '陽明', '富貴角'],
         '中部空品區':  ['豐原', '沙鹿', '大里', '忠明', '西屯', '彰化',
                         '線西', '二林', '南投', '竹山', '埔里'],
         '竹苗空品區':  ['湖口', '竹東', '新竹', '頭份', '苗栗', '三義'],
         '雲嘉南空品區':['斗六', '崙背', '新港', '朴子', '台西', '嘉義', 
                         '新營', '善化', '安南', '台南', '麥寮'],
         '高屏空品區':  ['美濃', '橋頭', '仁武', '大寮', '林園', '楠梓',
                         '左營', '前金', '前鎮', '小港', '屏東', '潮州', '恆春'],
         '宜蘭空品區':  ['宜蘭', '冬山'],
         '花東空品區':  ['台東', '花蓮', '關山'],
         '其他':        ['金門', '馬公', '馬祖']}

vars = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'NMHC']
Time = pd.date_range('2019/01/01', '2019/12/31', freq='1d')

for var in vars:
    Data = pd.DataFrame()
    for ston in stons:
        dataDir = os.path.join(pwd, 'RawData', ston)
        for st in stons[ston]:
            data = pd.read_csv(dataDir + '/' + st + '_2019.csv', 
                               delimiter='\s+\,', index_col=1, skiprows=[1], 
                               encoding='big5', engine='python')
            df = data.loc[data['測項']==var, '00':]
            df.index = pd.to_datetime(df.index, format='%Y/%m/%d %H:%M:%S')
            ttData = pd.DataFrame()
            for tt in Time:
                try:
                   ttdf = pd.Series(data=df.loc[tt], dtype='float')
                   ttdf.index = pd.date_range(tt, periods=24, freq='1h')
                except KeyError:
                   ttdf = pd.Series(index=pd.date_range(tt, periods=24, freq='1h'),
                                    dtype='float') 
                ttData = pd.concat([ttData, ttdf], axis=0, sort=False)
            ttData.columns = [st]
            Data = pd.concat([Data, ttData], axis=1, sort=False)

    Data = Data.replace(['#$','\*$','x$','A$','NA'], value=np.nan, regex=True)
    if (var=='NMHC'):
       Data = Data.astype(float)*1000
    Data = Data.fillna(-999)
    Data.index = [datetime.datetime.strftime(tt, '%Y-%m-%d-%H') for tt in Data.index]

    outFil = os.path.join(pwd, 'TaiwanData', '2019' + var + '_PerHour.csv')
    Data.to_csv(outFil, encoding='utf-8-sig')


