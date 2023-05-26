import xarray as xr

data = xr.open_dataset('2019_01/wrfout_d03_2019-01-01_12:00:00')
stons_d2 = {'首爾':[37.567, 126.967], '東京':[35.700, 139.750],
            '北京':[39.933, 116.283]}
d2latnmb = 168
d2lonnmb = 165
stons_d3 = {'濟州':[33.517, 126.533], '那霸':[26.200, 127.683],
            '上海':[31.400, 121.470], '福州':[26.083, 119.283], '廈門':[24.483, 118.083]}
d3latnmb = 222
d3lonnmb = 222

minval = {st:[] for st in stons_d3}
for st in stons_d3:
    print(st)
    limit = 100
    for lat in range(d3latnmb):
        for lon in range(d3lonnmb):
            dlat = abs(data['XLAT'][0, lat, lon] - stons_d3[st][0])
            dlon = abs(data['XLONG'][0, lat, lon] - stons_d3[st][1])
            minDD = (dlat**2+dlon**2)**0.5
            if minDD < limit:
               limit = minDD
               latlon = [lat, lon]
    print(limit)
    print(latlon)
    minval[st] = latlon
print(minval)

