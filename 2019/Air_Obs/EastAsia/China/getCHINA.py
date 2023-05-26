import requests
import csv
import pandas as pd
import datetime
from inlp.convert import chinese


start = '20190101'
end   = '20190823'
date = pd.date_range(start, end, freq='1d')
Date = [datetime.datetime.strftime(dd, '%Y%m%d') for dd in date]

#Data = pd.DataFrame()

for DD in Date:
#   src = 'https://quotsoft.net/air/'
    src = 'https://quotsoft.net/air/data/china_cities_' + DD + '.csv'

    response = requests.get(src)
    decoded_content = response.content.decode('utf-8') 

    cr = csv.reader(decoded_content.splitlines(), delimiter=',') 
    data = list(cr)
    columns = [chinese.s2t(cc) for cc in data[0]]
    df = pd.DataFrame(data[1:], columns=columns)
    df.set_index(['date'], inplace=True)
    print(df)

    df.to_csv('./RawData/china_cities_' + DD + '.csv', encoding = 'utf-8-sig')

    
