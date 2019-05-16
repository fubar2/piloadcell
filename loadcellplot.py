import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from dateutil import tz
from tzlocal import get_localzone
tzl = get_localzone().zone
iname = 'loadcell.xls' # 'loadcell_first17hours_4kg.xls'
df = pd.read_csv(iname,sep='\t')
df.columns=["epoch","mass"]
df['timestamp'] = pd.to_datetime(list(df['epoch']),unit='s')
df['date'] = pd.to_datetime(df['epoch'],unit='s',utc=True)
df.set_index(df['date'],inplace=True)
df = df.tz_localize(tz=tzl)

mdates.rcParams['timezone'] = tzl


lastone = df.iloc[-1].tolist()
lasttime = lastone[2].strftime('%Y%d%m_%H%M%S')
firstone = df.iloc[1].tolist()
firsttime = firstone[2].strftime('%Y%d%m_%H%M%S')
imname = 'loadcell%s.png' % (lasttime)
x = df['date']
y = df['mass']
ms = 2
nrow = df.shape[0]
if nrow > 1000:
    ms = 1
elif nrow > 10000:
    ms = 0.5
elif nrow > 100000:
    ms = 0.2
plt.figure(figsize=(10,8))
plt.plot(x, y, c='blue',linestyle='None', markersize = ms, marker='o')
plt.title('%d Loadcell values, %s to %s' % (nrow,firsttime,lasttime))
plt.xlabel('Time (usually as month-day hour)')
plt.ylabel('Reported Mass (g)')

plt.grid()

plt.savefig(imname, bbox_inches='tight')
plt.show()
