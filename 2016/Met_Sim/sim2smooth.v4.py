import xarray as xr
import pandas as pd
import numpy as np
import datetime
import os

### 溫度
def Temp(ds):    #每個測站的溫度資料

    t2 = (ds['T2'] - 273.15)
    t2.attrs['units'] = 'deg C'

    temp = {'馬祖':-999,            '彭佳嶼':t2[:,169,145], '鞍部': t2[:,153,127], '淡水': t2[:,153,124], 
            '竹子湖':t2[:,153,128], '基隆':t2[:,152,134],   '台北': t2[:,148,127], '新屋':t2[:,147,111], 
            '板橋':t2[:,147,124],   '新竹':t2[:,140,110],   '宜蘭':t2[:,138,135],  '蘇澳': t2[:,132,138], 
            '金門':-999,            '梧棲':t2[:,120,95],    '台中':t2[:,116,100],  '花蓮':t2[:,110,130], 
            '日月潭':t2[:,107,107], '澎湖':t2[:,95,63],     '阿里山':t2[:,93,104], '嘉義':t2[:,93,92], 
            '玉山':t2[:,92,109],    '東吉島':t2[:,84,67],   '成功':t2[:,79,123],   '永康':t2[:,76,85], 
            '台南':t2[:,75,84],     '台東':t2[:,66,115],    '高雄':t2[:,59,89],    '大武':t2[:,52,107],   
            '蘭嶼':t2[:,41,129],    '恆春':t2[:,39,102]}

    return temp


def wrfT2(df1, df2, ssList, LastSet):

    d1 = [round(x, 2) for x in np.linspace(1, 0, 12, endpoint=False)] # 1 -> 0 等差級數
    d2 = [round(x, 2) for x in np.linspace(0, 1, 12, endpoint=False)] # 0 -> 1 等差級數

    Tempt2 = pd.DataFrame()
    for st in ssList:
        if (st == '馬祖') or (st == '金門'):
           varSer = pd.DataFrame([-999 for a in range(0,37)])

        else:
           if (LastSet == True):                                 #若為END那一天 
              varSer = pd.DataFrame(df1[st][12:36].values)       #varSer由"第一筆第12hr-35hr"組成

           elif (LastSet == False):                              #若不為END那一天 則進行 smooth
              a1 = df1[st][24:36].values                         #a1:取第一筆第24hr-35hr
              a2 = df2[st][0:12].values                          #a2:取第二筆第0hr-11hr
 
              dfall = df1[st][12:24].values                      #取第一筆第12hr-23hr
              dfsmooth = a1*d1 + a2*d2                           #取a1及a2進行smooth

              varSer = pd.DataFrame(np.append(dfall, dfsmooth))  #varSer由"第一筆第12hr-23hr"及
                                                                 #"a1及a2進行smooth"組成

        Tempt2 = pd.concat([Tempt2, varSer], axis=1, sort=False)

    Tempt2.columns = ssList
    return Tempt2


### 風速風向
def Winds(ds):        #每個測站的U,V場資料
    u = (ds['U'])
    v = (ds['V'])
    u10 = (ds['U10'])
    v10 = (ds['V10'])


    winds= {'馬祖':-999,
            '彭佳嶼':[u10[:,169,145], v10[:,169,145]], '鞍部':[u10[:,153,127], v10[:,153,127]],
            '淡水':[u10[:,153,124], v10[:,153,124]],   '竹子湖':[u10[:,153,128], v10[:,153,128]],
            '基隆':[u[:,0,152,134], v[:,0,152,134]],   '台北':[u[:,0,148,127], v[:,0,148,127]], 
            '新屋':[u10[:,147,111], v10[:,147,111]],   '板橋':[u10[:,147,124], v10[:,147,124]],  
            '新竹':[u10[:,140,110], v10[:,140,110]],   '宜蘭':[u[:,0,138,135], v[:,0,138,135]],
            '蘇澳':[u[:,0,132,138], v[:,0,132,138]],   '金門':-999,    
            '梧棲':[u[:,0,120,95], v[:,0,120,95]],     '台中':[u10[:,116,100], v10[:,116,100]],
            '花蓮':[u10[:,110,130], v10[:,110,130]],   '日月潭':[u10[:,107,107], v10[:,107,107]],
            '澎湖':[u10[:,95,63], v10[:,95,63]],       '阿里山':[u10[:,93,104], v10[:,93,104]],
            '嘉義':[u10[:,93,92], v10[:,93,92]],       '玉山':[u10[:,92,109], v10[:,92,109]],   
            '東吉島':[u10[:,84,67], v10[:,84,67]],     '成功':[u10[:,79,123], v10[:,79,123]],  
            '永康':[u[:,0,76,85], v[:,0,76,85]],       '台南':[u[:,0,75,84], v[:,0,75,84]],   
            '台東':[u10[:,66,115], v10[:,66,115]],     '高雄':[u10[:,59,89], v10[:,59,89]],
            '大武':[u10[:,52,107], v10[:,52,107]],     '蘭嶼':[u10[:,41,129], v10[:,41,129]],  
            '恆春':[u10[:,39,102], v10[:,39,102]]} 

    return winds


def smooth(df1st, df2st, uv):          #進行smooth動作
    d1 = [round(x, 2) for x in np.linspace(1, 0, 12, endpoint=False)] # 1 -> 0 等差級數
    d2 = [round(x, 2) for x in np.linspace(0, 1, 12, endpoint=False)] # 0 -> 1 等差級數

    a1 = df1st[uv][24:36].values       #a1:取第一筆第24hr-35hr
    a2 = df2st[uv][0:12].values        #a2:取第二筆第0hr-11hr

    dfall = df1st[uv][12:24].values    #取第一筆第12hr-23hr
    dfsmooth = a1*d1 + a2*d2           #取a1及a2進行smooth

    return np.append(dfall, dfsmooth)  #經過smooth的新array


def wrfWS(df1, df2, ssList, LastSet):

    def cal_ws(uu, vv):                #將U,V進行風速計算
        cal = np.sqrt(uu**2+ vv**2)
        return cal 
       
    WS = pd.DataFrame()
    for st in ssList:
        if (st == '馬祖') or (st == '金門'):
           varSer = pd.DataFrame([-999 for a in range(0,37)])
        else:
           if (LastSet == True):         #若為END那一天，varSer由"第一筆第12hr-35hr"組成
             varSer = pd.DataFrame(cal_ws(df1[st][0][12:36].values, df1[st][1][12:36].values))
           elif (LastSet == False):      #若不為END那一天，varSer則由經過smooth的新array組成
             varSer = pd.DataFrame(cal_ws(smooth(df1[st], df2[st], 0), smooth(df1[st], df2[st], 1)))

        WS = pd.concat([WS, varSer], axis=1, sort=False)

    WS.columns = ssList
    return WS


def wrfWD(df1, df2, ssList, LastSet):

    def cal_wd(uu, vv):                #將U,V進行風向計算
        cal = []
        for i in range(0,24):
           if (abs(uu[i]) <= 1.E-3) and (vv[i] > 0):
              ddir = 90.
           elif (abs(uu[i]) <= 1.E-3) and (vv[i] < 0):
              ddir = 270.
           elif (uu[i] > 0 ):
              ddir = np.arctan(vv[i]/uu[i])*57.2957795
           elif (uu[i] < 0):
              ddir = np.arctan(vv[i]/uu[i])*57.2957795 + 180.0
 
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
           if (LastSet == True):         #若為END那一天，varSer由"第一筆第12hr-35hr"組成
             varSer = pd.DataFrame(cal_wd(df1[st][0][12:36].values, df1[st][1][12:36].values))
           elif (LastSet == False):      #若不為END那一天，varSer則由經過smooth的新array組成
             varSer = pd.DataFrame(cal_wd(smooth(df1[st], df2[st], 0), smooth(df1[st], df2[st], 1)))

        WD = pd.concat([WD, varSer], axis=1, sort=False)

    WD.columns = ssList
    return WD
   


## 主程式
def main():
    global ssList, vars, rootDir 
    ssList = ['鞍部', '淡水', '竹子湖', '基隆', '台北', '新屋'  , '板橋'  , '新竹',
              '宜蘭', '蘇澳', '梧棲'  , '台中', '花蓮', '日月潭', '阿里山', '嘉義',
              '玉山', '成功', '永康'  , '台南', '台東', '高雄'  , '大武'  , '恆春']

    vars =['T2','WS','WD']

    Start = datetime.datetime.strptime('2015-12-31', '%Y-%m-%d')
    End = datetime.datetime.strptime('2016-12-31', '%Y-%m-%d')

    rootDir = os.path.dirname(os.path.abspath(__file__))

    wrfStart  = (Start - pd.Timedelta('1d')).strftime('%Y-%m-%d')
    wrfEnd    = End.strftime('%Y-%m-%d')

    filenm = pd.date_range(start=wrfStart, end=wrfEnd, freq='1d').strftime('%Y-%m-%d')

    for i in range(1, len(filenm)):

        print(filenm[i])
        YMDir1 = (datetime.datetime.strptime(filenm[i-1], '%Y-%m-%d')    #第一筆資料夾及檔案位置設定
                  + pd.Timedelta('1d')).strftime('%Y_%m')
        InDir1  = os.path.join(rootDir, 'data_in', YMDir1)
        ds_1st = xr.open_dataset(InDir1+ '/wrfout_d04_' + filenm[i-1] + '_12:00:00' )

   
        if (filenm[i] == wrfEnd): # 若為END的那一天
           LastSet = True         # 則 LastSet 設為True
           ds_2nd = ds_1st

        else:                     # 若為END的那一天
           LastSet = False        # 則 LastSet 設為False
           YMDir2 = (datetime.datetime.strptime(filenm[i], '%Y-%m-%d')   #第二筆資料夾及檔案位置設定
                    + pd.Timedelta('1d')).strftime('%Y_%m')
           InDir2  = os.path.join(rootDir, 'data_in', YMDir2)
           ds_2nd = xr.open_dataset(InDir2+ '/wrfout_d04_' + filenm[i] + '_12:00:00' )


        smooth_var(ds_1st, ds_2nd, LastSet, filenm[i])  
        smooth_raw(ds_1st, ds_2nd, LastSet, filenm[i])



def smooth_var(ds_1st, ds_2nd, LastSet, filetime):

    for var in vars:
       nm = eval('wrf' + var)
       if (var == 'T2'):
          dfout = nm(Temp(ds_1st), Temp(ds_2nd), ssList, LastSet)
       else:
          dfout = nm(Winds(ds_1st), Winds(ds_2nd), ssList, LastSet)

       dfout.index = pd.date_range(start=filetime+'-00', 
                                   end=filetime+'-23', 
                                   freq='1h').strftime('%Y-%m-%d-%H')
       dfout.index.name = 'UTC'
#      print(dfout)

       OutDir = os.path.join(rootDir, 'data_out', var)
       try:
          os.makedirs(OutDir)
       except FileExistsError:
          pass
       csvfile = os.path.join(OutDir, filetime + '_' + var + '_sim.csv')
       dfout.to_csv(csvfile, encoding ='utf-8-sig')



def smooth_raw(ds_1st, ds_2nd, LastSet, filetime):
    d1 = [round(x, 2) for x in np.linspace(1, 0, 12, endpoint=False)]
    d2 = [round(x, 2) for x in np.linspace(0, 1, 12, endpoint=False)]

    if (LastSet == True):
       ds = xr.merge([ds_1st['U10'][12:36], ds_1st['V10'][12:36], ds_1st['Times'][12:36]])
       OutDir = os.path.join(rootDir, 'data_out', 'smooth_raw', filetime[:7])

    elif (LastSet == False):
       for i in range(12):
          ds_1st['U10'][i+24,:,:] = d1[i] * ds_1st['U10'][i+24,:,:] + \
                                    d2[i] * ds_2nd['U10'][i,:,:]
          ds_1st['V10'][i+24,:,:] = d1[i] * ds_1st['V10'][i+24,:,:] + \
                                    d2[i] * ds_2nd['V10'][i,:,:]
       ds = xr.merge([ds_1st['U10'][12:36], ds_1st['V10'][12:36], ds_1st['Times'][12:36]])


    OutDir = os.path.join(rootDir, 'data_out', 'smooth_raw', filetime[:7])
    try:
       os.makedirs(OutDir)
    except FileExistsError:
       pass
    ncfile = os.path.join(OutDir, 'wrfout_d04_U10V10_' + filetime)
    ds.to_netcdf(ncfile)


    if (filetime == '2016-01-01'):
       dz = xr.merge([ds_1st['U10'][0:12], ds_1st['V10'][0:12], ds_1st['Times'][0:12]])
       ncfile = os.path.join(OutDir, 'wrfout_d04_U10V10_' + '2015-12-31')
       dz.to_netcdf(ncfile)


if __name__ == '__main__':
    main()
