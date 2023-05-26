import pandas as pd

def Korea_ID(inFil):
   data = pd.read_excel(inFil, index_col=0, usecols=[0,1,4,5])
   data.columns = ['id', 'lat', 'lon']

   Sr = [37.33345, 37.57873, 126.8102, 127.1191]
   Xr = [33.47097, 33.55381, 126.4683, 126.5676]

   Sid = []
   Xid = []
   for df in range(len(data)):
       if (data['lat'][df]> Sr[0] and data['lat'][df]< Sr[1] and \
           data['lon'][df]> Sr[2] and data['lon'][df]< Sr[3]):
          Sid.append(data['id'][df])
       elif (data['lat'][df]> Xr[0] and data['lat'][df]< Xr[1] and \
             data['lon'][df]> Xr[2] and data['lon'][df]< Xr[3]):
          Xid.append(data['id'][df])

   return {'首爾':Sid, '濟州':Xid}
