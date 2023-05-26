import pandas as pd
import os,calendar

TTimes=pd.date_range('2019-01-01', '2020-01-01', freq='1h').strftime('%Y-%m-%d-%H')
columns = ['東京','沖繩']


###資料處理
#東京
Vars = {'O3':b'OX  ',   'NMHC':b'NMHC', 'NO2':b'NO2 ',\
        'PM10':b'SPM ', 'PM2.5':b'PM25', 'SO2':b'SO2 '}
TYFil = os.path.join(os.getcwd(), 'RawData', '2019_13104010.csv')
TYData = pd.read_csv(TYFil, encoding='SJIS')
TYData['測定項目コード'] = [tt.encode('UTF-8') for tt in TYData['測定項目コード']] 

#沖繩
Filnm = {'O3':'06', 'NO2':'03', 'PM10':'10', 'PM2.5':'12', 'SO2':'01'}
ONWDir = os.path.join(os.getcwd(), 'RawData', '47211050', '2019')



def VarPro(var, vData):

    outData = pd.DataFrame()
    for mn in range(12):
        mdData = vData[vData['測定月']==(mn+1)]
        for i in range(calendar.monthrange(2019, mn+1)[1]):
            Dtmpt = pd.Series(mdData.iloc[i, 7::])
            outData = pd.concat([outData, Dtmpt], axis=0, sort=False)
    if (var=='NMHC'):
       outData = outData*10
    outData = outData.replace([9998, 9999, 99980, 99990], -999)
    outData.index = TTimes[1:]
    outData.drop(TTimes[-1], axis=0, inplace=True)

    return outData



for var in Vars:
    FstData = pd.DataFrame(-999, index=[TTimes[0]], columns=columns)

    #東京
    TYvData = TYData[TYData['測定項目コード']==Vars[var]]
    TYDf = VarPro(var, TYvData)

    #沖繩
    try:
       ONWData = pd.read_csv(ONWDir+'/j472019_'+Filnm[var]+'.txt', encoding='SJIS')
       ONWvData = ONWData[ONWData['測定局コード']==47211050]
       ONWDf = VarPro(var, ONWvData)
    except KeyError:
       ONWDf =  pd.DataFrame(-999, index=TTimes[1:-1], columns=['沖繩'])

    DataOut = pd.concat([TYDf, ONWDf], axis=1, sort=False)
    DataOut.columns = columns
    DataOut = pd.concat([FstData, DataOut], axis=0)


    OutFil = os.path.join(os.getcwd(), 'JapanData', 'Japan_'+var+'.csv')
    DataOut.to_csv(OutFil, encoding='utf-8-sig')
