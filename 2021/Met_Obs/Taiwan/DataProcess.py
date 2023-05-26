import pandas as pd
import os, datetime

pwd = os.getcwd()

ssList = ['鞍部', '淡水', '竹子湖', '基隆', '台北', '新屋'  , '板橋'  , '新竹',
          '宜蘭', '蘇澳', '梧棲'  , '台中', '花蓮', '日月潭', '阿里山', '嘉義',
          '玉山', '成功', '永康'  , '台南', '台東', '高雄'  , '大武'  , '恆春']
vars = ['T2', 'WS', 'WD']

start = '2021-05-01'
end = '2021-07-31'
Times = pd.date_range(start, end, freq='1d').strftime('%Y-%m-%d')

for var in vars:
    print(var)
    inDir = os.path.join(pwd, 'data_in', var)

    allData = pd.read_csv(inDir + '/202104' + var + '.csv',
                           encoding='utf-8-sig', index_col=0)

    for tt in range(4, 8):
        data = pd.read_csv(inDir + '/2021' + '%02d' % (tt+1) + var + '.csv',
                           encoding='utf-8-sig', index_col=0)
        Data = pd.DataFrame()
        for st in ssList:
            stdf = pd.Series(data[st], name=st, index=data.index)
            Data = pd.concat([Data, stdf], axis=1, sort=False)
        allData = pd.concat([allData, Data], axis=0, sort=False)
    if (var== 'WD'):
       allData = allData.replace(['V','X','...','0',0], -999)
    else:
       allData = allData.replace(['V','X','...'], -999)
    print(allData)

    ### LTS -> UTC
    allData.index = pd.date_range('2021-04-30-01', '2021-08-02-00', freq='1h')-pd.Timedelta('8h')
   

    outDir = os.path.join(pwd, 'data_out', var)
    for dd in Times:
        outData = allData.loc[dd]
        outData.index = [datetime.datetime.strftime(dd, '%Y-%m-%d-%H') for dd in outData.index]
        outFil = os.path.join(outDir, dd + '_' + var + '_obs.csv')
        outData.to_csv(outFil, encoding='utf-8-sig')
#       print(outData)
