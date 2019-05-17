#! /usr/bin/python3
# stand alone plotter - currently just uses the growing output file
# but can be used on historical files by editing
# adjusted to accept an input xls file

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import time
import sys
import os
from dateutil import tz
from tzlocal import get_localzone

tzl = get_localzone().zone
mdates.rcParams['timezone'] = tzl

if (len(sys.argv) > 1):
    iname = sys.argv[1]
    ifilename, ifile_extension = os.path.splitext(iname)
    imname = '%s.png' % ifilename 
else:
    iname = 'loadcell.xls' # 'loadcell_first17hours_4kg.xls'
    imname = 'loadcell_%s.png' % (time.strftime('%Y%m%d%H%M%S',time.localtime()))

df = pd.read_csv(iname,sep='\t')

df.columns=["epoch","mass"]
df['date'] = pd.to_datetime(df['epoch'],unit='s')
df.set_index(df['date'],inplace=True)
df = df.tz_localize(tz=tzl)

lastone = df.epoch[-1]
lasttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(lastone))

firstone = df.epoch[0]
firsttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(firstone))

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
