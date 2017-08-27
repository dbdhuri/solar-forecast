#!/usr/bin/env python

import sys
sys.dont_write_bytecode=True

import datetime
import urllib
import numpy as np
import json
import time
import urllib
import glob
import csv
f_vals = []
f_vals_sum = []
missings = []
files = glob.glob('version3data/*.dat')

for ifk in xrange(0,len(files)):
    files[ifk] = files[ifk][13:]


for ifk in xrange(0,len(files)):
    f = files[ifk]
    print f
    fname = f[3:16]
    date= f[3:7]+'.'+f[7:9]+'.'+f[9:11]+'_'+f[12:14]+':'+f[14:16]+'_TAI'
    url_sharp = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=hmi.sharp_720s[][%s]&op=rs_list&key=HARPNUM,QUALITY,AREA,TOTUSJH,TOTPOT,TOTUSJZ,ABSNJZH,SAVNCPP,USFLUX,AREA_ACR,MEANPOT,R_VALUE,SHRGT45,MEANSHR,MEANGAM,MEANGBT,MEANGBZ,MEANGBH,MEANJZH,MEANJZD,MEANALP"%date
    response_sharp = urllib.urlopen(url_sharp)
    url_lorentz = "http://jsoc.stanford.edu/cgi-bin/ajax/jsoc_info?ds=cgem.lorentz[][%s]&op=rs_list&key=HARPNUM,QUALITY,TOTBSQ,TOTFZ,TOTFY,TOTFX,EPSZ,EPSY,EPSX"%date
    response_lorentz = urllib.urlopen(url_lorentz)
    data_sharp = json.loads(response_sharp.read())
    data_lorentz = json.loads(response_lorentz.read())
    all_this = []
    if response_sharp.getcode() == 200 and response_lorentz.getcode() == 200 and data_sharp['count']>0 and data_lorentz['count']>0:
        if data_sharp['keywords'][0]['values'] == data_lorentz['keywords'][0]['values']:
            for j in range(0,len(data_sharp['keywords'][0]['values'])):
                if int(data_sharp['keywords'][1]['values'][j],16) < 65536 and AREA > 200:
                    this = [fname]            
                    for i in range(3,len(data_sharp['keywords'])):
                        val = data_sharp['keywords'][i]['values'][j]
                        if val != 'MISSING' and np.isinf(float(val)) != 0:
                            this.append(float(data_sharp['keywords'][i]['values'][j]))
                    for i in range(2,len(data_lorentz['keywords'])):
                        val = data_lorentz['keywords'][i]['values'][j]
                        if val != 'MISSING' and np.isinf(float(val)) != 0:
                            this.append(float(data_lorentz['keywords'][i]['values'][j]))                
                    if len(this) == 26:
                        f_vals.append(this)
                        all_this.append(this)
    if len(all_this) > 0:
        this_sum = np.empty(len(this)-1)
        for i in range(0,len(this_sum)):
            for j in range(len(all_this)):
                this_sum[i] += all_this[j][i+1]
        f_vals_sum.append([fname] + list(this_sum))   
    else:
        missings.append(fname)

writer = csv.writer(open('HMI_features_201401_201406_ARwise_week.csv','w'))
writer.writerows(f_vals)
writer = csv.writer(open('HMI_features_201401_201406_week.csv','w'))
writer.writerows(f_vals_sum)
writer = csv.writer(open('HMI_features_201401_201406_missingdates_week.csv','w'))
writer.writerows(missings)


data = csv.reader(open('HMI_features_201401_201406.csv','r'))
data = list(data)

crop_data = []

for item in data:
    if len(item) == 26:
        crop_data.append(item)

print 'crop..', len(crop_data)

set_dates = []

for item in crop_data:
    set_dates.append(item[0][:-5])

set_dates = list(set(set_dates))
print 'set_dates.', len(set_dates)
print set_dates[0]

select_terms = []
count_s = 0
for i in range(0,len(set_dates)):
    print i
    s = '_0900'                    
    found = 0                      
    while found == 0 and int(s[1:3])<= 15:    
         date_s = set_dates[i] + s         
         for item in crop_data:     
             if item[0] == date_s:
                 count_s += 1 
                 select_terms.append(date_s)
                 found = 1    
                 break                  
         secs = int(s[3:5]) + 12        
         s = s[:3] + '%02d'%secs           
         if secs == 60:                 
             secs = 0                      
             s = '_%02d'%(int(s[1:3])+1) + '%02d'%secs 


print 'st..', len(select_terms)
print 'counts..', count_s

new_data = []
for item in crop_data:
    if item[0] in select_terms:
        new_data.append(item)

print 'new..', len(new_data)
print new_data[0][0][:-5]

writer = csv.writer(open('HMI_features_201401_201406_sorted.csv','w'))
writer.writerows(new_data)
 
missing_dates = []

start_date = datetime.datetime.strptime('20140101','%Y%m%d')
end_date = datetime.datetime.strptime('20140630','%Y%m%d')

while start_date <= end_date:
    date_s = datetime.datetime.strftime(start_date,'%Y%m%d')
    print date_s
    found = 0
    for item in new_data:
       if item[0][:-5] == date_s:
           found = 1 
           break
    if found == 0:
        missing_dates.append([date_s])
    start_date += datetime.timedelta(seconds=24*3600)

print 'missings.', len(missing_dates)
writer = csv.writer(open('HMI_features_201401_201406_sorted_missings.csv','w'))
writer.writerows(missing_dates)


d = csv.reader(open('HMI_features_201401_201406_sorted.csv','r'))
d=list(d)
print len(d)


#for i in range(len(d)):
#    if len(d[i]) == 26:
#        count +=
#print lens
for i in range(1,len(d[0])):
    print i
    this = np.empty(len(d))
    for j in range(0,len(d)):
        this[j] = d[j][i]
    this = sorted(this)
    for j in range(0,len(this)):
        if np.isinf(this[j]) == 0:
            min_index = j
            break
    for j in range(len(this)-1,-1,-1):
        if np.isinf(this[j]) == 0:
            max_index = j
            break
    for j in range(0,len(d)):
        if np.isinf(this[j]):
            if this[j] < 0.0:
                this[j] = this[min_index]
            elif this[j] > 0.0:
                this[j] = this[max_index]
    mean = np.mean(this)
    stv = np.std(this)
    fl = open('Means_STDs.txt','a')
    fl.write('%0.4e %0.4e %0.4e %0.4e\n'%(mean,stv,this[min_index],this[max_index]))
    fl.close()
