import pandas as pd
import os
from os import listdir,environ
import numpy as np
import datetime
import re
from datetime import date, timedelta
from sys import argv
import seaborn as sns

#location
App_location =  'E:/....'
#getting start and end date
start = date.today()  - timedelta(7)
end = date.today()  - timedelta(1)

#get the list of App_location
App_Dates = os.listdir(App_location)
#App_Dates to dataFrame rename the columns and drop the last index
df = pd.DataFrame(App_Dates,columns={'File_name'}).iloc[:-1]
#New Date column
df['Date'] = None

inedx_fname = df.columns.get_loc('File_name')
#get the date and file name from our DataFrame
inedx_date = df.columns.get_loc('Date')
#get the date parten from string
date_pattern = r'([0-9]{4}-[0-9]{2}-[0-9]{2})'

#get only numbers from string from our DataFrame
for row in range(0, len(df)):
    #serach and group
    date = re.search(date_pattern,df.iat[row ,inedx_fname]).group()
    df.iat[row, inedx_date] = date

#get the size of our file size
size = []
for folder in sorted(os.listdir(App_location)):
    #get size
    filesize = os.path.getsize(App_location+folder)
    #append
    size.append(filesize)
App_sizef = pd.DataFrame(size, columns={'File_size'})

#concartenate our DataFrame
conFrames = pd.concat([df,App_sizef], axis=1)

#convert our Date string from DataFrame to date
conFrames['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d")

#drop column File_name from our DataFrame since we have extracted date in it, set our Date field to index and also drop duplicates
Last7Days =  conFrames.drop(columns=['File_name']).set_index(['Date']).iloc[:-1].drop_duplicates().tail(7)

#get missing date from our DataFrame
dif =pd.date_range(start = start, end = end).difference(Last7Days.index)
pd.DataFrame(dif,columns={'Missing Date'})

#plot our Date and file size
ax = sns.barplot(data = Last7Days.reset_index(), x = 'Date', y = 'File_size')
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")