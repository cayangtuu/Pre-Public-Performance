import xarray as xr
import pandas as pd
import numpy as np
import datetime
import os

def wrfT2(ds, ssList):

    t2 = (ds['T2'] - 273.15)
    t2.attrs['units'] = 'deg C'

    temp = {'馬祖':-999,            '彭佳嶼':t2[:,169,145], '鞍部': t2[:,153,127], '淡水站': t2[:,153,124], 
            '竹子湖':t2[:,153,128], '基隆':t2[:,152,134],   '台北': t2[:,148,127], '新屋':t2[:,147,111], 
            '板橋':t2[:,147,124],   '新竹':t2[:,140,110],   '宜蘭':t2[:,138,135],  '蘇澳': t2[:,132,138], 
            '金門':-999,            '梧棲':t2[:,120,95],   '台中':t2[:,116,100],  '花蓮':t2[:,110,130], 
            '日月潭':t2[:,107,107], '澎湖':t2[:,95,63],     '阿里山':t2[:,93,104], '嘉義':t2[:,93,92], 
            '玉山':t2[:,92,109],    '東吉島':t2[:,84,67],   '七股':t2[:,80,81],    '成功':t2[:,79,123],
            '永康':t2[:,76,85],     '台南':t2[:,75,84],     '台東':t2[:,66,115],   '高雄':t2[:,59,89], 
            '大武':t2[:,52,107],    '蘭嶼':t2[:,41,129],    '恆春':t2[:,39,102]}

    Tempt2 = pd.DataFrame()
    for st in ssList:
        if (st == '馬祖') or (st == '金門'):
           varSer = pd.DataFrame([-999 for a in range(0,37)])
        else:
           varSer = temp[st].to_dataframe()['T2']
        Tempt2 = pd.concat([Tempt2, varSer], axis=1, sort=False)

    Tempt2.columns = ssList
    return Tempt2


def wrfWS(ds, ssList):
    u = (ds['U'])
    v = (ds['V'])
    u10 = (ds['U10'])
    v10 = (ds['V10'])


    winds= {'馬祖':-999,
            '彭佳嶼':[u10[:,169,145], v10[:,169,145]], '鞍部':[u10[:,153,127], v10[:,153,127]],
            '淡水站':[u10[:,153,124], v10[:,153,124]], '竹子湖':[u10[:,153,128], v10[:,153,128]],
            '基隆':[u[:,0,152,134], v[:,0,152,134]],  '台北':[u[:,0,148,127], v[:,0,148,127]], 
            '新屋':[u10[:,147,111], v10[:,147,111]],  '板橋':[u10[:,147,124], v10[:,147,124]],  
            '新竹':[u10[:,140,110], v10[:,140,110]],  '宜蘭':[u[:,0,138,135], v[:,0,138,135]],
            '蘇澳':[u[:,0,132,138], v[:,0,132,138]],  '金門':-999,    
            '梧棲':[u[:,0,120,95], v[:,0,120,95]],     '台中':[u10[:,116,100], v10[:,116,100]],
            '花蓮':[u10[:,110,130], v10[:,110,130]],   '日月潭':[u10[:,107,107], v10[:,107,107]],
            '澎湖':[u10[:,95,63], v10[:,95,63]],       '阿里山':[u10[:,93,104], v10[:,93,104]],
            '嘉義':[u10[:,93,92], v10[:,93,92]],       '玉山':[u10[:,92,109], v10[:,92,109]],   
            '東吉島':[u10[:,84,67], v10[:,84,67]],      '七股':[u10[:,80,81], v10[:,80,81]],
            '成功':[u10[:,79,123], v10[:,79,123]],     '永康':[u[:,0,76,85], v[:,0,76,85]],   
            '台南':[u[:,0,75,84], v[:,0,75,84]],       '台東':[u10[:,66,115], v10[:,66,115]],  
            '高雄':[u10[:,59,89], v10[:,59,89]],       '大武':[u10[:,52,107], v10[:,52,107]],   
            '蘭嶼':[u10[:,41,129], v10[:,41,129]],     '恆春':[u10[:,39,102], v10[:,39,102]]} 

    def cal_ws(uv):
        cal = np.sqrt(uv[0]**2+ uv[1]**2)
        return cal 
       
    WS = pd.DataFrame()
    for st in ssList:
        if (st == '馬祖') or (st == '金門'):
           varSer = pd.DataFrame([-999 for a in range(0,37)])
        else:
            varSer = pd.DataFrame(cal_ws(winds[st]).values)
        WS = pd.concat([WS, varSer], axis=1, sort=False)

    WS.columns = ssList
    return WS


def wrfWD(ds, ssList):
    u = (ds['U'])
    v = (ds['V'])
    u10 = (ds['U10'])
    v10 = (ds['V10'])

    winds= {'馬祖':-999,
            '彭佳嶼':[u10[:,169,145], v10[:,169,145]], '鞍部':[u10[:,153,127], v10[:,153,127]],
            '淡水站':[u10[:,153,124], v10[:,153,124]], '竹子湖':[u10[:,153,128], v10[:,153,128]],
            '基隆':[u[:,0,152,134], v[:,0,152,134]],  '台北':[u[:,0,148,127], v[:,0,148,127]], 
            '新屋':[u10[:,147,111], v10[:,147,111]],  '板橋':[u10[:,147,124], v10[:,147,124]],  
            '新竹':[u10[:,140,110], v10[:,140,110]],  '宜蘭':[u[:,0,138,135], v[:,0,138,135]],
            '蘇澳':[u[:,0,132,138], v[:,0,132,138]],  '金門':-999,    
            '梧棲':[u[:,0,120,95], v[:,0,120,95]],     '台中':[u10[:,116,100], v10[:,116,100]],
            '花蓮':[u10[:,110,130], v10[:,110,130]],   '日月潭':[u10[:,107,107], v10[:,107,107]],
            '澎湖':[u10[:,95,63], v10[:,95,63]],       '阿里山':[u10[:,93,104], v10[:,93,104]],
            '嘉義':[u10[:,93,92], v10[:,93,92]],       '玉山':[u10[:,92,109], v10[:,92,109]],   
            '東吉島':[u10[:,84,67], v10[:,84,67]],      '七股':[u10[:,80,81], v10[:,80,81]],
            '成功':[u10[:,79,123], v10[:,79,123]],     '永康':[u[:,0,76,85], v[:,0,76,85]],   
            '台南':[u[:,0,75,84], v[:,0,75,84]],       '台東':[u10[:,66,115], v10[:,66,115]],  
            '高雄':[u10[:,59,89], v10[:,59,89]],       '大武':[u10[:,52,107], v10[:,52,107]],   
            '蘭嶼':[u10[:,41,129], v10[:,41,129]],     '恆春':[u10[:,39,102], v10[:,39,102]]} 

    def cal_wd(uv):
        cal = []
        for i in range(0,37):
           if (abs(uv[0][i]) <= 1.E-3) and (uv[1][i] > 0):
              ddir = 90.
           elif (abs(uv[0][i]) <= 1.E-3) and (uv[1][i] < 0):
              ddir = 270.
           elif (uv[0][i] > 0 ):
              ddir = np.arctan(uv[1][i]/uv[0][i])*57.2957795
           elif (uv[0][i] < 0):
              ddir = np.arctan(uv[1][i]/uv[0][i])*57.2957795 + 180.0
 
           dir = 270.-ddir
           if (dir < 0.):
              dir = dir+360.
           if (dir > 360.):
              dir = dir-360.

           cal.append(dir)
        return cal  


    WD = pd.DataFrame()
    for st in ssList:
        if (st == '馬祖') or (st == '金門'):
           varSer = pd.DataFrame([-999 for a in range(0,37)])
        else:
           varSer = pd.DataFrame(cal_wd(winds[st]))
        WD = pd.concat([WD, varSer], axis=1, sort=False)

    WD.columns = ssList
    return WD
   


##進行smooth處理及計算

def smooth(df1, df2):
   d1 = pd.Series([round(x, 2) for x in np.linspace(1, 0, 12, endpoint=False)])
   d2 = pd.Series([round(x, 2) for x in np.linspace(0, 1, 12, endpoint=False)])

   a1 = df1.iloc[24:36, :]
   a1.index=[x for x in range(12)]
   a2 = df2.iloc[0:12, :]
   a2.index=[x for x in range(12)]

   b1 = a1.mul(d1, axis=0)
   b2 = a2.mul(d2, axis=0)

   return b1+b2



ssList = ['鞍部', '淡水站', '竹子湖', '基隆', '台北', '新屋'  , '板橋'  , '新竹',
          '宜蘭', '蘇澳'  , '梧棲'  , '台中', '花蓮', '日月潭', '阿里山', '嘉義',
          '玉山', '七股'  , '成功'  , '永康', '台南', '台東'  , '高雄'  , '大武', '恆春']

vars =['T2','WS','WD']

Start = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d')
End = datetime.datetime.strptime('2016-12-31', '%Y-%m-%d')

rootDir = os.path.dirname(os.path.abspath(__file__))

wrfStart  = (Start - pd.Timedelta('1d')).strftime('%Y-%m-%d')
wrfEnd    = End.strftime('%Y-%m-%d')

filenm = pd.date_range(start=wrfStart, end=wrfEnd, freq='1d').strftime('%Y-%m-%d')

for var in vars:
   print(var)
   for i in range(1, len(filenm)):

      print(filenm[i])
      if (filenm[i] != wrfEnd): #不為END的那一天
        YMDir1 = (datetime.datetime.strptime(filenm[i-1], '%Y-%m-%d') + pd.Timedelta('1d')).strftime('%Y_%m')
        InDir1  = os.path.join(rootDir, 'data_in', YMDir1)
        ds_1st = xr.open_dataset(InDir1+ '/wrfout_d04_' + filenm[i-1] + '_12:00:00' )

        YMDir2 = (datetime.datetime.strptime(filenm[i], '%Y-%m-%d') + pd.Timedelta('1d')).strftime('%Y_%m')
        InDir2  = os.path.join(rootDir, 'data_in', YMDir2)
        ds_2nd = xr.open_dataset(InDir2+ '/wrfout_d04_' + filenm[i] + '_12:00:00' )
   
        nm = eval('wrf' + var)
        df1 = nm(ds_1st, ssList)
        df2 = nm(ds_2nd, ssList)

        dfall = df1.iloc[12:24, :]
        dfsmooth = smooth(df1,df2) 
        dfout = pd.concat([dfall, dfsmooth], axis=0, sort=False)


      else:                     #若為END的那一天
        YMDir1 = (datetime.datetime.strptime(filenm[i-1], '%Y-%m-%d') + pd.Timedelta('1d')).strftime('%Y_%m')
        InDir1  = os.path.join(rootDir, 'data_in', YMDir1)
        ds_1st = xr.open_dataset(InDir1+ '/wrfout_d04_' + filenm[i-1] + '_12:00:00' )
        nm = eval('wrf' + var)
        df = nm(ds_1st, ssList)

        dfout = df.iloc[12:36, :]


      dfout.index = pd.date_range(start=filenm[i]+'-00', 
                                  end=filenm[i]+'-23', 
                                  freq='1h').strftime('%Y-%m-%d-%H')
#     print(dfout)

      OutDir = os.path.join(rootDir, 'data_out', var)
      try:
         os.makedirs(OutDir)
      except FileExistsError:
         pass
      csvfile = os.path.join(OutDir, filenm[i] + '_' + var + '_sim.csv')
      dfout.to_csv(csvfile, encoding ='utf-8-sig')


