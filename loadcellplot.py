#! /usr/bin/python3
# stand alone plotter - currently just uses the growing output file
# but can be used on historical files by editing
# adjusted to accept an input xls file

import pandas as pd
import numpy as np

import matplotlib as mpl
mpl.use('Agg') # headless!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import time
import sys
import os
import io
import copy
from dateutil import tz
from tzlocal import get_localzone

tzl = get_localzone().zone
mdates.rcParams['timezone'] = tzl
NSD = 2.0
IGSEC = None
# arbitrary hack - throw away data until load cell settles down a bit
# need more data to see if makes a useful difference

class loadCellPlotter():

    def __init__(self,nsd,infi):
        self.started = time.time()
        self.tzl = tzl
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
        df = df.tz_localize(tz=self.tzl)
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
        """ trim +/-nsd SD and ignore first IGSEC data as load cell settles a bit
        """
        if IGSEC:
            begn = self.df.iloc[0,0] + IGSEC
            oldc = self.nrow
            print('begn=',begn)
            i = 0
            while (i < self.nrow) and (self.df.epoch[i] < begn):
                i += 1
            if i < self.nrow:
                self.df = self.df.iloc[i:,:]
                self.nrow = self.df.shape[0]
            print('### Started with %d. After igsec, have %d rows' % (oldc,self.nrow))
        firstone = self.df.iloc[0,0]
        firsttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(firstone))
        lastone = self.df.iloc[-1,0] # easier to use the original epoch rather than the internal datetimes!
        lasttime = time.strftime('%H:%M:%S %d/%m/%Y',time.localtime(lastone))
        self.fstamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(lastone))
        self.firsttime = firsttime
        self.lasttime = lasttime  
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


    def loadcellplotFlask(self):
        bytes_image = io.BytesIO()
        mdates.rcParams['timezone'] = self.tzl
        imname = 'loadcell%s.png' % (self.lasttime)
        x = self.df['date']
        y = self.df['mass']
        plt.figure(figsize=(10,8),dpi=150)
        plt.plot(x, y, c='blue',linestyle='None', markersize = self.ms, marker='o')
        titl = '%d Loadcell values from %s to %s' % (self.nrow,self.firsttime,self.lasttime)
        plt.title(self.subt,fontsize=14)
        plt.suptitle(titl,fontsize=17, y=0.985)
        plt.xlabel('Date/Time (month-day hour for example)')
        plt.ylabel('Reported Mass (g)')
        plt.grid()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image

    def loadcellplot(self,imname):
        mdates.rcParams['timezone'] = tzl
        x = self.df['date']
        y = self.df['mass']
        plt.figure(figsize=(10,8),dpi=150)
        plt.plot(x, y, c='blue',linestyle='None', markersize = self.ms, marker='o')
        titl = '%d Loadcell values from %s to %s' % (self.nrow,self.firsttime,self.lasttime)
        plt.title(self.subt,fontsize=14)
        plt.suptitle(titl,fontsize=17, y=0.985)
        plt.xlabel('Date/Time (month-day hour for example)')
        plt.ylabel('Reported Mass (g)')
        plt.grid()
        plt.savefig(imname, bbox_inches='tight')
        plt.show()
        plt.close()

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        iname = sys.argv[1]
        ifilename, ifile_extension = os.path.splitext(iname)
        imf = '%s.png' % ifilename 
    else:
        iname = 'loadcell.xls' # 'loadcell_first17hours_4kg.xls'
        imf = 'loadcell_%s.png' % (time.strftime('%Y%m%d_%H%M%S',time.localtime()))

    lc = loadCellPlotter(nsd=NSD,infi=iname)
    lc.loadcellplot(imf)
