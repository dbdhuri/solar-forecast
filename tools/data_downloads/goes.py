#!/usr/bin/env python

import sys
sys.dont_write_bytecode=True
import csv
import urllib
import pickle
import calendar
import datetime
can = calendar.Calendar()


baseurl = "https://satdat.ngdc.noaa.gov/sem/goes/data/new_full/"
data = [] #Main List Object Format [[time_tag, Quality_Flag, B_Count, B_Flux]]

Eras = [['20100101','20101027',14],['20101028','20121022',15],['20121023','20121118',14],['20121119','20150520',15],['20150521','20150608',14],['20150609','20160502',15],['20160503','20160511',13],['20160512','20160608',14],['20160609','20180331',15]]

for i in range(0,len(Eras)):
    era = Eras[i]
    date = datetime.datetime.strptime(era[0],'%Y%m%d') 
    end_date = datetime.datetime.strptime(era[1],'%Y%m%d')
    print type(date), type(end_date)
    while date <= end_date:
        date_s = datetime.datetime.strftime(date,'%Y%m%d')
        print date_s
        GOES = era[2]
        url = baseurl + "%d/%02d/goes%d/csv/g%d_xrs_2s_%s_%s.csv" %(date.year,date.month,GOES,GOES,date_s,date_s)
        response = urllib.urlopen(url)
        status_data = response.getcode()
        GOES = 15
        while status_data != 200 and GOES > 12:
            GOES -= 1
            url = baseurl + "%d/%02d/goes%d/csv/g%d_xrs_2s_%s_%s.csv" %(date.year,date.month,GOES,GOES,date_s,date_s)
            response = urllib.urlopen(url)
            status_data = response.getcode()
        GOES = era[2]
        if status_data == 200:  
            thisdata=list(csv.reader(response))
            for start in xrange(len(thisdata)):
                if len(thisdata[start]) > 0 and thisdata[start][0] == 'time_tag':
                    break                        
            for i in xrange(start+1,len(thisdata)):
                if len(thisdata[i]) == 7:
                    Quality_Flag = int(thisdata[i][4])
                    B_count = float(thisdata[i][5])
                    B_Flux = float(thisdata[i][6])
                    if Quality_Flag == 0 and B_count != -99999.0 and B_Flux != -99999.0:
                        thisdate = thisdata[i][0][:-4]
                        data.append([thisdate, Quality_Flag, B_count, B_Flux])
        date += datetime.timedelta(hours=24)       

writer = csv.writer(open('../../data/Flux_data_Source.csv','w'))
writer.writerows(data)

print 'done..'
