import xarray as xr
import pandas as pd
import numpy as np
import datetime
import os

### 溫度
def Temp(ds):    #每個測站的溫度資料

    t2 = (ds['T2'] - 273.15)
    t2.attrs['units'] = 'deg C'

#   temp = {'首爾':t2[:,119,88], '東京':t2[:,116,130], '北京': t2[:,129,54]} 
    temp = {'濟州':t2[:,208,170], '那霸機場':t2[:,121,187], '上海': t2[:,181,120],
            '福州': t2[:,117,97], '廈門': t2[:,98,84]} 

    return temp


def wrfT2(df1, df2, ssList, LastSet):

    d1 = [round(x, 2) for x in np.linspace(1, 0, 12, endpoint=False)] # 1 -> 0 等差級數
    d2 = [round(x, 2) for x in np.linspace(0, 1, 12, endpoint=False)] # 0 -> 1 等差級數

    Tempt2 = pd.DataFrame()
    for st in ssList:
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
    u10 = (ds['U10'])
    v10 = (ds['V10'])


#   winds = {'首爾':[u10[:,119,88], v10[:,119,88]], '東京':[u10[:,116,130], v10[:,116,130]],
#            '北京':[u10[:,129,54], v10[:,129,54]]} 
    winds = {'濟州':[u10[:,208,170], v10[:,208,170]], '那霸機場':[u10[:,121,187],v10[:,121,187]],
             '上海':[u10[:,181,120], v10[:,181,120]], '福州':[u10[:,117,97], v10[:,117,97]], 
             '廈門':[u10[:,98,84], v10[:,98,84]]} 

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
#   ssList = ['首爾', '東京', '北京']
    ssList = ['濟州', '那霸機場', '上海', '福州', '廈門']

    vars =['T2','WS','WD']

    Start = datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')
    End = datetime.datetime.strptime('2019-12-31', '%Y-%m-%d')

    rootDir = os.getcwd()

    wrfStart  = (Start - pd.Timedelta('1d')).strftime('%Y-%m-%d')
    wrfEnd    = End.strftime('%Y-%m-%d')

    filenm = pd.date_range(start=wrfStart, end=wrfEnd, freq='1d').strftime('%Y-%m-%d')

    for i in range(1, len(filenm)):

        print(filenm[i])
        YMDir1 = (datetime.datetime.strptime(filenm[i-1], '%Y-%m-%d')    #第一筆資料夾及檔案位置設定
                  + pd.Timedelta('1d')).strftime('%Y_%m')
        InDir1  = os.path.join(rootDir, 'data_in', YMDir1)
        ds_1st = xr.open_dataset(InDir1+ '/wrfout_d03_' + filenm[i-1] + '_12:00:00' )

   
        if (filenm[i] == wrfEnd): # 若為END的那一天
           LastSet = True         # 則 LastSet 設為True
           ds_2nd = ds_1st

        else:                     # 若為END的那一天
           LastSet = False        # 則 LastSet 設為False
           YMDir2 = (datetime.datetime.strptime(filenm[i], '%Y-%m-%d')   #第二筆資料夾及檔案位置設定
                    + pd.Timedelta('1d')).strftime('%Y_%m')
           InDir2  = os.path.join(rootDir, 'data_in', YMDir2)
           ds_2nd = xr.open_dataset(InDir2+ '/wrfout_d03_' + filenm[i] + '_12:00:00' )


        smooth_var(ds_1st, ds_2nd, LastSet, filenm[i])  



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

       OutDir = os.path.join(rootDir, 'data_out', 'D3', var)
       try:
          os.makedirs(OutDir)
       except FileExistsError:
          pass
       csvfile = os.path.join(OutDir, filetime + '_' + var + '_sim.csv')
       dfout.to_csv(csvfile, encoding ='utf-8-sig')


if __name__ == '__main__':
    main()
