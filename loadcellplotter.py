# module for the flask server - returns an image to display

import pandas as pd
import matplotlib as mpl
mpl.use('Agg') # headless!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

import datetime
from dateutil import tz
from tzlocal import get_localzone
import time

tzl = get_localzone().zone
trimci = 2.0 # set None for no trim

def trimcl(df,nsd):
    mene = df.mass.mean()
    ci = df.mass.std()*2.0
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
    return(df2,s,s2)


def loadcellplot():
    df = pd.read_csv('loadcell.xls',sep='\t')
    df.columns=["epoch","mass"]
    df['date'] = pd.to_datetime(df['epoch'],unit='s')
    df.set_index(df['date'],inplace=True)
    df = df.tz_localize(tz=tzl)
    if trimci:
        df,note,descr = trimcl(df,trimci)
    mdates.rcParams['timezone'] = tzl
    lastone = df.epoch[-1] # easier to use the original epoch rather than the internal datetimes!
    lasttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(lastone))
    firstone = df.epoch[0]
    firsttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(firstone))
    imname = 'loadcell%s.png' % (lasttime)
    x = df['date']
    y = df['mass']
    ms = 2
    nrow = df.shape[0]
    if nrow > 1000:
        ms = 1
    if nrow > 10000:
        ms = 0.5
    if nrow > 100000:
        ms = 0.2
    plt.figure(figsize=(10,8),dpi=150)
    plt.plot(x, y, c='blue',linestyle='None', markersize = ms, marker='o')
    titl = '%d Loadcell values from %s to %s' % (df.shape[0],firsttime,lasttime)
    if trimci:
        plt.title(note,fontsize=14)
        plt.suptitle(titl,fontsize=17, y=0.985)
    else:
        plt.title(titl)
    plt.xlabel('Date/Time (month-day hour for example)')
    plt.ylabel('Reported Mass (g)')
    plt.grid()
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    plt.close()
    bytes_image.seek(0)
    return bytes_image

