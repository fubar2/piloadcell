# module for the flask server - returns an image to display
# updated to a class able to cache the last image

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

import datetime
from dateutil import tz
from tzlocal import get_localzone
import time

tzl = get_localzone().zone

class loadCellPlotter():

    def __init__(self,nsd,infi):
        self.nsd = nsd
        self.have_cache = False
        if infi:
            self.infile = infi
        else:
            self.infile = 'loadcell.xls'
        df = pd.read_csv(self.infile,sep='\t')
        df.columns=["epoch","mass"]
        df['date'] = pd.to_datetime(df['epoch'],unit='s')
        df.set_index(df['date'],inplace=True)
        df = df.tz_localize(tz=tzl)
        self.df = df
        ms = 2
        nrow = self.df.shape[0]
        if nrow > 1000:
            ms = 1
        if nrow > 10000:
            ms = 0.5
        if nrow > 100000:
            ms = 0.2
        self.ms = ms
        self.nrow = nrow
        self.trimcl()
 
    def trimcl(self):
        if self.nsd:
            mene = self.df.mass.mean()
            ci = self.df.mass.std()*self.nsd
            ucl = mene + ci
            lcl = mene - ci
            notbig = self.df.mass < ucl
            df2 = self.df[notbig]
            notsmall = df2.mass > lcl
            df2 = df2[notsmall]
            nhi = sum(notbig==False)
            nlo = sum(notsmall==False)
            s = 'Trim +/- %.1f SD removed %d above %.2f and %d below %.2f\n' % (self.nsd,nhi,ucl,nlo,lcl)
            s2 = '##Before trim:\n %s\nAfter trim:\n %s' % (self.df.describe(),df2.describe())
            self.df = df2
        else:
            s = 'Raw untrimmed data'
            s2 = '##Raw:\n%s' % (self.df.describe())
        self.note = s2
        self.subt = s


    def loadcellplot(cached=True,keep=True):
        if cached and self.have_cache:
            return self.bytes_image
        else:
            bytes_image = io.BytesIO()
            mdates.rcParams['timezone'] = tzl
            lastone = self.df.epoch[-1] # easier to use the original epoch rather than the internal datetimes!
            lasttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(lastone))
            firstone = self.df.epoch[0]
            firsttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(firstone))
            imname = 'loadcell%s.png' % (lasttime)
            lasttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(lastone))
            x = self.df['date']
            y = self.df['mass']
            plt.figure(figsize=(10,8),dpi=150)
            plt.plot(x, y, c='blue',linestyle='None', markersize = self.ms, marker='o')
            titl = '%d Loadcell values from %s to %s' % (self.nrow,firsttime,lasttime)
            plt.title(self.subt,fontsize=14)
            plt.suptitle(titl,fontsize=17, y=0.985)
            plt.xlabel('Date/Time (month-day hour for example)')
            plt.ylabel('Reported Mass (g)')
            plt.grid()
            plt.savefig(bytes_image, format='png')
            plt.close()
            bytes_image.seek(0)
            if self.keep:
                self.bytes_image = bytes_image
                self.have_cache = True
            return bytes_image

