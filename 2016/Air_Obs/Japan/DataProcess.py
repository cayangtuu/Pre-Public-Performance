import pandas as pd
import datetime
import calendar
import os

Time = pd.date_range('2016-01-01-01', '2017-01-01-00', freq='1h')
TTime = [datetime.datetime.strftime(tt, '%Y-%m-%d-%H') for tt in Time]

def ReadData(data):
    outData = pd.DataFrame() 
    for mn in range(12):
       df = data[data['month']==(mn+1)]
       for i in range(calendar.monthrange(2016,mn+1)[1]):
          Dtmpt = pd.Series(df.iloc[i, 4::]) 
          outData = pd.concat([outData, Dtmpt], axis=0, sort=False)

    outData.index = TTime
    outData.drop('2017-01-01-00', axis=0, inplace=True)

    return outData


data= pd.read_csv('2016_13104010.csv', header=None, encoding='utf-8-sig')
data = data.iloc[:, 3::]

columns=['speci', 'units', 'month', 'date']
for i in range(24):
    columns.append(str(i+1)+'h')
data.columns = columns


# Tokyo O3
data_o3 = data.iloc[1860:2232, :]
Tokyo_o3 = ReadData(data_o3)
Tokyo_o3.columns = ['東京']

# Tokyo PM10
data_pm10 = data.iloc[3348:3720, :]
Tokyo_pm10 = ReadData(data_pm10)
Tokyo_pm10.columns = ['東京']

#Okinawa_O3
Odata_o3= pd.read_csv('j472016_06.txt', encoding='utf-8-sig')
Odata_o3 = Odata_o3.iloc[:, 3::]
Odata_o3.columns = columns
Okinawa_o3 = ReadData(Odata_o3)
Okinawa_o3.columns = ['沖繩']

#Okinawa_PM10
Odata_pm10= pd.read_csv('j472016_10.txt', encoding='utf-8-sig')
Odata_pm10 = Odata_pm10.iloc[:, 3::]
Odata_pm10.columns = columns
Okinawa_pm10 = ReadData(Odata_pm10)
Okinawa_pm10.columns = ['沖繩']

O3_Data = pd.concat([Tokyo_o3, Okinawa_o3], axis=1, sort=False)
O3_Data = O3_Data.replace([9998, 9999], -999)
#O3_Data.to_csv('Japan_O3.csv', encoding= 'utf-8-sig')

PM10_Data = pd.concat([Tokyo_pm10, Okinawa_pm10], axis=1, sort=False)
PM10_Data = PM10_Data.replace([9998, 9999], -999)
#PM10_Data.to_csv('Japan_PM10.csv', encoding= 'utf-8-sig')

#--------------------------------------------------------------------------
MM = input('月: ') 
LD = input('最後一天: ') 
YM = '2016-'+MM
start = '2016-'+MM+'-01-00'
end = '2016-'+MM+'-'+LD+'-23'
rootDir = os.path.dirname(os.path.abspath(__file__))
fileDir = os.path.join(rootDir, YM)

df_o3 = pd.read_csv(fileDir+'/2016'+MM+'O3_PerHour.csv', encoding= 'utf-8-sig')
df_o3.columns = ['time', '首爾', '濟州', '東京', '沖繩', '北京', '上海', '福州', '廈門']
df_o3.set_index('time', inplace=True)
df_o3.drop(['東京', '沖繩'], axis=1, inplace=True)

dd_o3 = pd.concat([df_o3.iloc[:, 0:2], O3_Data.loc[start:end, :], df_o3.iloc[:, 2::]],
                  axis=1, sort=False)
dd_o3 = dd_o3.replace([np.nan], -999)
dd_o3.to_csv(fileDir+'/new-2016'+MM+'O3_PerHour.csv', encoding= 'utf-8-sig')
print(dd_o3)

df_pm10 = pd.read_csv(fileDir+'/2016'+MM+'PM10_PerHour.csv', encoding= 'utf-8-sig')
df_pm10.columns = ['time', '首爾', '濟州', '東京', '沖繩', '北京', '上海', '福州', '廈門']
df_pm10.set_index('time', inplace=True)
df_pm10.drop(['東京', '沖繩'], axis=1, inplace=True)

dd_pm10 = pd.concat([df_pm10.iloc[:, 0:2], PM10_Data.loc[start:end, :], df_pm10.iloc[:, 2::]],
                    axis=1, sort=False)
dd_pm10 = dd_pm10.replace([np.nan], -999)
dd_pm10.to_csv(fileDir+'/new-2016'+MM+'PM10_PerHour.csv', encoding= 'utf-8-sig')
print(dd_pm10)
