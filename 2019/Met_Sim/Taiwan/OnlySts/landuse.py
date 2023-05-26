import xarray
dataDir = '/home/cayang/DataProcess/2019/Met_Sim/data_in/2019_01/'
dataFil = 'wrfout_d04_2019-01-30_12:00:00'
data = xarray.open_dataset(dataDir+dataFil)
LU = data['LU_INDEX']

stons = {'彭佳嶼':LU[0,169,145], '鞍部':LU[0,153,127], '淡水':LU[0,153,124],
         '竹子湖':LU[0,153,128], '基隆':LU[0,152,134], '台北':LU[0,148,127], '新屋':LU[0,147,111],
         '板橋':LU[0,147,124],   '新竹':LU[0,140,110], '宜蘭':LU[0,138,135], '蘇澳':LU[0,132,138],
         '梧棲':LU[0,120,95],    '台中':LU[0,116,100], '花蓮':LU[0,110,130],
         '日月潭':LU[0,107,107], '澎湖':LU[0,95,63], '阿里山':LU[0,93,104],  '嘉義':LU[0,93,92],
         '玉山':LU[0,92,109],    '東吉島':LU[0,84,67], '成功':LU[0,79,123],  '永康':LU[0,76,85],
         '台南':LU[0,75,84],     '台東':LU[0,66,115],  '高雄':LU[0,59,89],   '大武':LU[0,52,107],
         '蘭嶼':LU[0,41,129],    '恆春':LU[0,39,102]}

lu_cat = {1: 'Evergreen Needeleleaf Forest',  2: 'Evergreen Broadlesf Forest', 
          3: 'Deciduous Needleleaf Forest',   4: 'Deciduous Broadlesf Forest', 
          5: 'Mixed Forest',                  6: 'Closed Shrubland', 
          7: 'Open Shrubland',                8: 'Woody Savanna', 
          9: 'Savanna',                      10: 'Grassland', 
         11: 'Permanents Wetland',           12: 'Cropland',
         13: 'Urban and Built-up',           14: 'Cropland/Natural Mosaic', 
         15: 'Snow and Ice',                 16: 'Barren or Sparsely Vegetated',
         17: 'Water',                        18: 'Wooded Tundra', 
         19: 'Mixed Tundra',                 20: 'Barren Tundra'}

for ston in stons:
    for lu in lu_cat:
        if stons[ston].values == lu:
           print(f'{ston}: {stons[ston].values}     {lu_cat[lu]}')
