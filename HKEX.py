# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 23:38:05 2018

@author: hanwe
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 22:26:19 2017

@author: hanwe
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:26:43 2017

@author: hanwe
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import datetime
from calendar import monthrange

def inputyear(yearlow):
    year = input("Input the year with the format of 4 digits(only years smaller or equal to current year and larger or equal to " +str(yearlow) + " are accessible):")
    return year
def inputmonth(year):
    if year == "2017":
        mon = "03"
    else:
        mon = "01"
    month = input("Input the month with the format of 2 digits:\n(For startmonth:only months smaller or equal to 12 or current month and larger or equal to " + mon + " are accessible\nFor endmonth: only months larger or equal to startmonths and smaller or equal to 12 or current month are accessible)")
    return month
def inputday():
    day = input("Input the day with the format of 2 digits:(all need to be smaller than today's date)")
    return day
def dayrange(daylow,dayup,day, month, year, case, date, now):
    while int(daylow) > int(day) or int(dayup) < int(day):
        print("Wrong input. Please enter again.")
        day = inputday()
    newdate = [year, month, day]
    return newdate
        
def monrange(monlow, monup, month, year, case, date, now):
    while int(monlow) > int(month) or int(monup) < int(month):
        print("Wrong input. Please enter again.")
        month = inputmonth(year)
    day = inputday()
    #year = 2017 and month = 03
    if int(year) == 2017 and int(month) == 3:
        #start
        if case == 0:
            newdate = dayrange("17","31",day,month,year,case,date,now)
        #end
        else:
            newdate = dayrange(date[2],"31",day,month,year,case,date,now)
    #month larger than 03
    else:
        #start
        if case == 0:
            #startmonth and startyear are the same as current month and year
            if int(year) == now.year and int(month) == now.month:
                newdate = dayrange("01",str(now.day-1),day,month,year,case,date,now)
            #not the same
            else:
                newdate = dayrange("01", str(monthrange(int(year),int(month))[1]), day, month,year,case,date,now)
        #end
        else:
            #endmonth and endyear are the same as current month and year
            if int(year) == now.year and int(month) == now.month:
                #endmonth and endyear are the same as startmonth and startyear
                if year == date[0] and month == date[1]:
                    newdate = dayrange(date[2],str(now.day-1),day,month,year,case,date,now)
                else:
                    newdate = dayrange("01",str(now.day-1),day,month,year,case,date,now)
            #not the same
            else:
                newdate = dayrange("01", str(monthrange(int(year),int(month))[1]), day, month,year,case,date,now)      
    return newdate
            
def yearrange(yearlow, yearup, year,case, date, now):
    while int(yearlow) > int(year) or int(yearup) < int(year):
        #while int(year) != int(yearlow):
            print("Wrong input. Please enter again.")
            year = inputyear(yearlow) 
    #year = 2017
    if int(year) == 2017:
        month = inputmonth(year)
        #start
        if case == 0:
            newdate = monrange("03", "12", month, year, case,date, now)
        #end
        else:
            newdate = monrange(date[1],"12", month, year, case,date, now)
    #yearlow < yearup
    else:
        month = inputmonth(year)
        #start
        if case == 0:
            #current year
            if year == now.year:
                newdate = monrange("01",str(now.month),month, year, case, date, now)
            #non-current year
            else:
                newdate = monrange("01","12", month, year, case, date, now)
        #end
        else:
            #startyear and endyear in the same year
            if date[0] == year:
                #current year
                if year == now.year:
                    newdate = monrange(date[1],str(now.month),month, year, case, date, now)
                #non-current year
                else:
                    newdate = monrange(date[1],"12", month, year, case, date, now) 
            #startyear and endyear not in the same year
            else:
                #current year
                if year == now.year:
                    newdate = monrange("01",str(now.month),month, year, case, date, now)
                #non-current year
                else:
                    newdate = monrange("01","12", month, year, case, date, now)
    return newdate
#scrape the data from a specified date and write them into a csv file with name according to the date
def get(day,month,year,url,datasource,addr):
    #sess=requests.Session()
    res=requests.get(url)
    data = res.text
    bs = BeautifulSoup(data, "lxml")
    __EVENTVALIDATION = bs.find("input", {"id": "__EVENTVALIDATION"}).attrs['value']
    __VIEWSTATEGENERATOR = bs.find("input", {"id": "__VIEWSTATEGENERATOR"}).attrs['value']
    __VIEWSTATE = bs.find("input", {"id": "__VIEWSTATE"}).attrs['value']
    today = bs.find("input", {"id": "today"}).attrs['value']
    data = {
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "today":today,
            "sortBy" : "",
            "alertMsg" : "",
            "ddlShareholdingDay":day,
            "ddlShareholdingMonth":month,
            "ddlShareholdingYear":year,
            "btnSearch.x": "2",
            "btnSearch.y": "1"
            }
    
    
    req = requests.post(url, data)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    all_tables=[[td.text for td in tr.find_all('td')] for tr in soup.find_all('tr',attrs={'class':re.compile('row[10]')})]
    stock_info=[[sub_item.replace('\r\n', '') for sub_item in item] for item in all_tables]
    i = 1
    df = pd.DataFrame({"Stock code":[stock_info[0][0]], "Stock Name": [stock_info[0][1]], "Shareholding in CCASS" : [stock_info[0][2]], "Shares Percentage" : [stock_info[0][3]]})
    for stock in stock_info[1:]:
        df2= pd.DataFrame({"Stock code":[stock_info[i][0]], "Stock Name": [stock_info[i][1]], "Shareholding in CCASS" : [stock_info[i][2]], "Shares Percentage" : [stock_info[i][3]]})
        i = i + 1
        df = df.append(df2,ignore_index = True)
    df.to_csv(addr + os.sep + datasource + str(year) + str(month) + str(day) + '.csv')
    print(datasource + str(year+month+day) + ".csv is completed.")
def getyear(startdate,enddate,url,datasource,addr):
    for years in range(int(startdate[0]),int(enddate[0]) + 1):
        #first year
        if years == int(startdate[0]):
            #first year equals last year
            if startdate[0] == enddate[0]:
                getmonth(startdate,enddate,str(startdate[1]),str(enddate[1]),addtwo(str(years)),url,datasource,addr)
            else:
                getmonth(startdate,enddate,str(startdate[1]),"12",addtwo(str(years)),url,datasource,addr)
        #last year
        elif years == int(enddate[0]):
            getmonth(startdate,enddate,"01",str(enddate[1]),addtwo(str(years)),url,datasource,addr)
        #other years
        else:
            getmonth(startdate,enddate,"01","12",addtwo(str(years)),url,datasource,addr)

def getmonth(startdate,enddate,startmon,endmon,year,url,datasource,addr):
    for months in range(int(startmon),int(endmon) + 1):
        #first month in first year
        if int(year) == int(startdate[0]) and months == int(startmon):
            #if first month equals last month
            if startdate[0] == enddate[0] and startmon == endmon:
                getday(startdate,enddate,str(startdate[2]),str(enddate[2]),addtwo(str(year)),addtwo(str(months)),url,datasource,addr)
            else:         
                getday(startdate,enddate,str(startdate[2]),str(monthrange(int(year),int(months))[1]),addtwo(str(year)),addtwo(str(months)),url,datasource,addr)
        #last month in last year
        elif int(year) == int(enddate[0]) and months == int(endmon):
            getday(startdate,enddate,"01",str(enddate[2]),addtwo(str(year)),addtwo(str(months)),url,datasource,addr)
        #other months
        else:
            getday(startdate,enddate,"01",str(monthrange(int(year),int(months))[1]),addtwo(str(year)),addtwo(str(months)),url,datasource,addr)

def getday(startdate,enddate,startday,endday,year,month,url,datasource,addr):
    for days in range(int(startday),int(endday) + 1):
        get(addtwo(str(days)),month,year,url,datasource,addr)
#add to two digits
def addtwo(a):
    if len(a) < 2:
        a = "0" + a
    return a
#main function starts here
now = datetime.datetime.now()
startday = "17"
startmonth = "03"
startyear = "2017"
endday = str(now.day)
endmonth = str(now.month)
endyear = str(now.year)
#data source seslection
while True:
    datasource = input("Select source of data(Input with 1, 2 or 3):\n1.Southbound shareholding through Shanghai and Shenzhen Connect\n2.Northbound shareholding through Shenzhen Connect\n3.Northbound shareholding through Shanghai Connect\n")
    if datasource == "1":
        url = "http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk"
        datasource = "Southbound shareholding through Shanghai and Shenzhen Connect"
        break
    elif datasource == "2":
        url = "http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz"
        datasource = "Northbound shareholding through Shenzhen Connect"
        break
    elif datasource == "3":
        url = "http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh"
        datasource = "Northbound shareholding through Shanghai Connect"
        break
    else:
        print("Wrong input.Please select again.")
#customized period
print("\nNotice: the oldest data could only be accessed is exactly one year from today. Access to previous data would incur error.")
while True:
    try:
        print("\nStartyear")
        startyear = input("Input the year with the format of 4 digits(only years smaller or equal to current year and larger or equal to 2017 are accessible):")
        date = [startyear, startmonth, startday]
        startdate = yearrange("2017",str(now.year), startyear,0,date, now)
        print("\nEndyear")
        endyear = input("Input the year with the format of 4 digits(only years smaller or equal to current year and larger or equal to " + startdate[0] + " are accessible):")
        enddate = yearrange(startdate[0],str(now.year), endyear,1,startdate, now)   
        addr = input("input your address to save files:")  
        getyear(startdate,enddate,url,datasource,addr)
        break
    except IndexError:
        print("\nNotice: the oldest data could only be accessed is exactly one year from today. Access to previous data would incur error. Try again.")