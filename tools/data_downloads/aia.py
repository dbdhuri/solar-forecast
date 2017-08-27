#!/usr/bin/env python

import sys
sys.dont_write_bytecode=True

import datetime
import urllib
from astropy.io import fits
import numpy as np
import json
import pickle
import time
import urllib
#date = datetime.datetime.strptime('2012.02.21_00:00:00','%Y.%m.%d_%H:%M:%S')
#end_date = datetime.datetime.strptime('2012.03.11_00:00:00','%Y.%m.%d_%H:%M:%S')
#
#start_time = time.time()
#
##big_d = []
#count = 0
#while date < end_date:
#    date_s = datetime.datetime.strftime(date,'%Y.%m.%d_%H:%M:%S')
#    url = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=aia.lev1[%s_TAI/12s][?WAVELNTH=171?]&op=rs_list&key=T_REC&seg=image_lev1"%date_s
#    print url
#    response = urllib.urlopen(url)
#    data = json.loads(response.read())
#    filename = data['segments'][0]['values'][0]
#    url = "http://jsoc.stanford.edu"+filename
#    chromosphere_image = fits.open(url)
#    chromosphere_image.verify("fix")
#    chromosphere_image[1].data.dump('AIA_171/%03d_%s_171_4096_4096.dat'%(count,date_s))
#    date += datetime.timedelta(seconds=3600)
#    count += 1
#
##    d = np.load('AIA_171/171_%s_4096.dat'%date_s)
##    big_d.append(d)
##    print date
##    date += datetime.timedelta(seconds=3600)
##
##big_d = np.array(big_d, dtype = np.int16)
##np.save(file('123.dat','w'),big_d)
##print time.time() - start_time
#print count

date = datetime.datetime.strptime('20140127_1348','%Y%m%d_%H%M')
end_date = datetime.datetime.strptime('20140630_0000','%Y%m%d_%H%M')

start_time = time.time()

aia_ls = [94,131,171,193,211,304,335,1600]
count = 3189
missing_dates = []
while date <= end_date:
    date_s = datetime.datetime.strftime(date,'%Y%m%d_%H%M')
    data = []
    is_complete = 1
    for aia_l in aia_ls:
        url = "http://jsoc.stanford.edu/data/aia/synoptic/%d/%02d/%02d/H%02d00/AIA%s_%04d.fits"%(date.year, date.month, date.day, date.hour,date_s,aia_l)
        print url
        response = urllib.urlopen(url)
        if response.getcode() == 200: 
            chromosphere_image = fits.open(url)
            chromosphere_image.verify("fix")
            #chromosphere_image[1].data *= 16.0
            data.append(chromosphere_image[1].data)
        else:
            is_complete = 0
            missing_dates.append(date_s)
            break
    if is_complete:
        data = np.array(data, dtype = np.int16)
        np.save(file('AIA_data_2014/%05d_%s_AIA_%02d_1024_1024.dat'%(count,date_s,len(aia_ls)),'w'),data)
    date += datetime.timedelta(seconds=720)
    count += 1

writer = csv.writer(open('AIA_data_2014/missing_dates.csv','w'))
writer.writerows(missing_dates)
print count

