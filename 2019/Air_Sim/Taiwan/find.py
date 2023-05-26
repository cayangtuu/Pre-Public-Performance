import xarray as xr
import pandas as pd

data = xr.open_dataset('GRIDCRO2D_Taiwan.nc')
sts = pd.read_csv('st.csv', index_col=0, encoding='utf-8-sig')
stons = {st:[float(sts.loc[sts['ch_name']==st, 'lat']), \
             float(sts.loc[sts['ch_name']==st, 'lon'])] for st in sts['ch_name']}
d4latnmb = 131
d4lonnmb = 92

minval = {st:[] for st in stons}
for st in stons:
    print(st)
    limit = 100
    for lat in range(d4latnmb):
        for lon in range(d4lonnmb):
            dlat = abs(data['LAT'][0, 0, lat, lon] - stons[st][0])
            dlon = abs(data['LON'][0, 0, lat, lon] - stons[st][1])
            minDD = (dlat**2+dlon**2)**0.5
            if minDD < limit:
               limit = minDD
               latlon = [lat+1, lon+1]
    minval[st] = latlon
print(minval)

