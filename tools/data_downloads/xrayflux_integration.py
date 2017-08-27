#!/usr/bin/env python

import sys
sys.dont_write_bytecode=True
import csv
import datetime
import time
import json
import numpy as np

#['2010-01-01 00:02:00', '6.2712e-08', '58']


class Y_lists:

#sum:
#weighted_sum_N:
#max_N
#log
#normal
    def __init__(self, file_path = '../../data/sw/Flux_2010_2017_max.csv',start_date = '2014-01-01 00:00:00' , end_date = '2014-06-30 23:48:00', lag=36, duration=60, trans = 'norm', func = 'maxN', vals = 1):
        self.start_date = start_date
        self.end_date = end_date
        self.lag = lag
        self.duration = duration
        self.trans = trans
        self.func = func
        self.data = csv.reader(open(file_path,'r'))
        self.data = list(self.data)
        self.init_date = datetime.datetime.strptime(self.data[1][0],'%Y-%m-%d %H:%M:%S')
        self.start_index = self.get_index(self.start_date)
        self.end_index = self.get_index(self.end_date)
        #self.__str__()
       
        
        if vals is not None:
	    self.val = vals
 
    def get_index(self, date_s):
        date = datetime.datetime.strptime(date_s,'%Y-%m-%d %H:%M:%S')
        delta = date-self.init_date
        delta = delta.days*24*30 + delta.seconds/120 + 1
        assert self.data[delta][0] == date_s
        delta += self.lag/2  
        return int(delta)

    def __str__(self):
        print 'Y_lists(file_path = ../../data/sw/Flux_2010_2017_max.csv,start_date = 2010-01-01 00:02:00 , end_date = 2014-12-31 23:48:00, lag=1, duration=12, trans = norm, func = maxN, vals = 1)'
        print 'file_path - Stored Flux data path'
        print 'lag - after Input image time in minutes'
        print 'duration - Integration period in minutes'
        print 'trans - transformatation on data norm or log'
        print 'func - selecting y data "maxN":maximum N values, "sum":Sum of all values, "weighted_sum": weighted sum of N values'
        print 'vals - N for maxN and weighted_sum'
  
    def print_result(self):
        print 'start_date', self.start_date
        print 'end_date', self.end_date
        print 'lag', self.lag
        print 'duration',self.duration
        print 'trans',self.trans 
        print 'func',self.func
         
    def agg_func(self):
        if self.func == 'maxN':
            Y_data = {}
            Y = []
            missing_dates = []
            #max_val = float(self.data[self.start_index][1])
            #min_val = float(self.data[self.start_index][1])
            max_val = 0.0
            min_val = 1.0
            print 'Finding..'
            for i in range(self.start_index, self.end_index+1, 6):
                print self.data[i]
                this_arr = []
                for j in range(i,i+self.duration/2):
                    if self.data[j][1] != 'NA':
                        this_arr.append(float(self.data[j][1]))
                    else:
                        this_arr.append(0.0)
             
                this_arr = sorted(this_arr, reverse=True)
                this_sum = 0.0
                assert self.val <= len(this_arr)
                for j in range(0,self.val):
                    this_sum += this_arr[j]   
                       
                this_date_s = 'AIA'+self.data[i-self.lag/2][0][:4]+self.data[i-self.lag/2][0][5:7]+self.data[i-self.lag/2][0][8:10]+'_'+self.data[i-self.lag/2][0][11:13]+self.data[i-self.lag/2][0][14:16]
                Y_data[this_date_s] = [this_sum]
                if this_sum == 0.0:
                    missing_dates.append([this_date_s[3:]])
                else:
                    Y.append([this_date_s[3:],this_sum])
                    if this_sum > max_val:
                       max_val = this_sum
                       max_date = this_date_s[3:]
                    elif this_sum < min_val:
                       min_val = this_sum
                       min_date = this_date_s[3:]
 
            print 'Storing'
            if self.duration >= 60:
                drt = self.duration/60
                drt_s = 'hr'
            else:
                drt = self.duration
                drt_s = 'min' 
            if self.lag >= 60:
                lgg = self.lag/60
                lgg_s = 'hr'
            else:
                lgg = self.lag
                lgg_s = 'min' 
            json.dump(Y_data, file('Y_flux.json','w'))
            writer = csv.writer(open('Ys_201401_201406/Y_missing_values_201401_201406_%02d%sDELAY_%02d%sMAX.csv'%(lgg,lgg_s, drt,drt_s),'w'))
            writer.writerows(missing_dates)
            writer = csv.writer(open('Ys_201401_201406/Y_GOES_XRAY_201401_201406_%02d%sDELAY_%02d%sMAX.csv'%(lgg, lgg_s, drt, drt_s),'w'))
            writer.writerows(Y)
            #Y=np.array(Y,dtype=np.float)
            #np.save(open('Y_GOES_XRAY_20140101_20140131.dat','w'),Y)
            
         
        return max_val, min_val, len(Y), len(missing_dates)
                  

L = [0,12,24,36,60,60*24]
D = [12,24,36,60,24*60]
for drs in D:
    for lgs in L:
        c = Y_lists(lag=lgs, duration=drs)
        mx, mn, lY, lm = c.agg_func()
        fl = open('Ys_201401_201406/Info.txt','a')
        fl.write('D=%d L=%d max=%0.4e min=%0.4e len_Y=%d len_m=%d\n'%(drs,lgs,mx,mn,lY,lm))
        fl.close()

#data = csv.reader(open('../../data/sw/Flux_2010_2017_max.csv','r'))
#data = list(data)






#def get_date_index(date_s):
#    date = datetime.datetime.strptime(date_s,'%Y-%m-%d %H:%M:%S')
#    delta = date - datetime.datetime.strptime('2010-01-01 00:02:00','%Y-%m-%d %H:%M:%S')
#    delta = delta.days*24*60/2 + delta.seconds/120 + 1
#    return delta
    
#start_date = '2014-01-01 00:00:00'
#end_date = '2014-06-30 23:58:00'
#
#def get_start_index(date):
#    
#
#pl.title("Bin_counts")
#counts = []
#for i in xrange(1,len(data)-6):
#    this_count = 0
#    for j in xrange(i,i+6):
#        if data[j][1] != 'NA':
#            this_count += 1
#    counts.append(this_count)
#
#print len(counts)
#
#import numpy as np
#counts = np.array(counts)
#for i in range(0,10):
#    print i, (counts == i).sum()
#hist, edges = np.histogram(counts,bins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5])
#print hist
#print edges
#pl.hist(counts)
#pl.show()
#pl.savefig('hist.png')
#pl.close()
#date = datetime.datetime.strptime('2014-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
#end_date = datetime.datetime.strptime('2014-06-30 23:58:00','%Y-%m-%d %H:%M:%S')




#T = 60 #Minutes
#data = list(data)
#
#fluxes = []
#date += datetime.timedelta(seconds = T*60)
#end_date += datetime.timedelta(seconds = T*60)
#def sep_date_elements(date_str):
#    year = int(date_str[:4])
#    month = int(date_str[5:7])
#    day = int(date_str[8:10])
#    hour = int(date_str[11:13])
#    minute = int(date_str[14:16])
#    second = int(date_str[17:19])
#    return (year, month, day, hour, minute, second)
#
#def find_index(start,this_date):
#    for i in range(start, len(data)):
#        (year, month, day, hour, minute, second) = sep_date_elements(data[i][0])
#        if year > this_date.year:
#            break
#        elif year == this_date.year and month > this_date.month: 
#            break
#        elif year == this_date.year and month == this_date.month and day > this_date.day:
#            break
#        elif year == this_date.year and month == this_date.month and day == this_date.day and hour > this_date.hour:
#            break
#        elif year == this_date.year and month == this_date.month and day == this_date.day and hour == this_date.hour and minute > this_date.minute:
#            break
#        elif  year == this_date.year and month == this_date.month and day == this_date.day and hour == this_date.hour and minute == this_date.minute and second > this_date.second:
#            break
#    return i
#    
#start_index = find_index(0,date)
#
#while date <= end_date:
#    print date
#    dateto = date + datetime.timedelta(seconds = T*60)
#    end_index = find_index(start_index, dateto)
#    max_val = 0.0
#    #print start_index, end_index
#    for i in range(start_index, end_index):
#        if float(data[i][3]) > max_val:
#            max_val = float(data[i][3])
#    fluxes.append([date, max_val])
#    start_index = end_index
#    date = dateto
#
#
#writer = csv.writer(open('Y_2014.csv','w'))
#writer.writerows(fluxes)

