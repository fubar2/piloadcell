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
trimci = 2.0

def trimcl(df,nsd):
    if nsd:
        mene = df.mass.mean()
        ci = df.mass.std()*nsd
        ucl = mene + ci
        lcl = mene - ci
        notbig = df.mass < ucl
        df2 = df[notbig]
        notsmall = df2.mass > lcl
        df2 = df2[notsmall]
        nhi = sum(notbig==False)
        nlo = sum(notsmall==False)
        s = 'Trim +/- %.1f SD removed %d above %.2f and %d below %.2f\n' % (nsd,nhi,ucl,nlo,lcl)
        s2 = '##Before trim:\n %s\nAfter trim:\n %s' % (df.describe(),df2.describe())
    else:
        s = 'Raw untrimmed data'
        s2 = '##Raw:\n%s' % df.describe()
        df2 = df
    return(df2,s,s2)
    
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
df,note,descr = trimcl(df,trimci)
print(descr)
lastone = df.epoch[-1]
lasttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(lastone))

firstone = df.epoch[0]
firsttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(firstone))

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
plt.rcParams["figure.figsize"] = (10,8)
plt.figure(dpi=150)
plt.plot(x, y, c='blue',linestyle='None', markersize = ms, marker='o')
titl = '%d Loadcell values, %s to %s' % (nrow,firsttime,lasttime)
if trimci:
    plt.title(note,fontsize=14)
    plt.suptitle(titl,fontsize=17, y=0.985)
else:
    plt.title(titl)
plt.xlabel('Time (usually as month-day hour)')
plt.ylabel('Reported Mass (g)')

plt.grid()

plt.savefig(imname, bbox_inches='tight')
plt.show()
plt.close()
