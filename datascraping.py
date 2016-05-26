"""
This set of functions is used to mine data from the Streak for the Cash game.
This is a histogram of 1000 tests:
    40 buckets:
    [109, 347, 405, 398, 313, 338, 378, 340, 301, 326, 367, 302, 250, 262, 275, 211, 163, 188, 197, 170, 180, 204, 176, 194, 208, 298, 320, 263, 312, 383, 400, 344, 357, 471, 423, 380, 469, 511, 449, 183]
    20 buckets:
    [456, 803, 651, 718, 627, 669, 512, 486, 351, 367, 384, 370, 506, 583, 695, 744, 828, 803, 980, 632]
    10 buckets:
    [1259, 1369, 1296, 998, 718, 754, 1089, 1439, 1631, 1612]
"""

import urllib2

daypmonth=[None,31,28,31,30,31,30,31,31,30,31,30,31]
year=2008
month=8
day=25

def nextdate():
    global year, month, day
    day+=1
    if day>daypmonth[month]:
        day=1
        month+=1
        if month>12:
            month=1
            year+=1

def getdate():
    global year, month, day
    syear=str(year)
    smonth=None
    if month<10:
        smonth="0"+str(month)
    else:
        smonth=str(month)
    sday=None
    if day<10:
        sday="0"+str(day)
    else:
        sday=str(day)
    return syear+smonth+sday

def scrap(n):
    rtn=[]
    for i in range(n):
        data=urllib2.urlopen('http://streak.espn.go.com/en/?date='+getdate()).read()
        win='http://g.espncdn.com/s/minigames/i/streak/arrow_left.gif'
        winfound=False
        for j in range(len(data)):
            if win==data[j:j+len(win)]:
                winfound=True
            if winfound and data[j:j+6]=='="wpw"':
                if data[j+11]=='%':
                    rtn.append(round(float(data[j+7:j+11])*10)/1000)
                else:
                    rtn.append(round(float(data[j+7:j+10])*10)/1000)
                winfound=False
        nextdate()
        if n>100 and not(n%10):
            print(str(round(float(i)/n*100))+'&')
    return rtn

def scrap2(n):
    rtn=[]
    for i in range(n):
        data=urllib2.urlopen('http://streak.espn.go.com/en/?date='+getdate()).read()
        getWinPercentage=False
        getQuestion=None
        getSport=None
        getHeatIndex=None
        getTime=None
        for j in range(len(data)):
            if data[j:j+17]=='matchup-container':
                if rtn[-1][0]==None:
                    del rtn[-1]
                rtn.append([None]*5);
            elif data[j:j+14]=='arrow_left.gif':
                getWinPercentage=True
            elif data[j-23:j]=='"gamequestion"><strong>':
                getQuestion=j
            elif data[j-19:j]=='sport-description">':
                getSport=j
            elif data[j-12:j]=='matchup had ':
                getHeatIndex=j
            elif data[j-9:j]=='eastern="':
                getTime=j
            if getWinPercentage and data[j:j+6]=='="wpw"':
                if data[j+11]=='%':
                    rtn[-1][0]=round(float(data[j+7:j+11])*10)/1000
                else:
                    rtn[-1][0]=round(float(data[j+7:j+10])*10)/1000
                getWinPercentage=False
            if getQuestion and data[j]=='<':
                rtn[-1][1]=data[getQuestion:j]
                getQuestion=None
            if getSport and data[j]=='<':
                rtn[-1][2]=data[getSport:j]
                getSport=None
            if getHeatIndex and data[j]=='%':
                rtn[-1][3]=round(float(data[getHeatIndex:j])*10)/1000
                getHeatIndex=None
            if getTime and data[j]=='"':
                rtn[-1][4]=data[getTime:j]
                getTime=None
        nextdate()
        if n>10 and not(n%10):
            print(str(round(float(i)/n*100))+'&')
    return rtn

def hist(data,buckets):
    rtn=[0]*buckets
    for i in range(len(data)):
        if data[i]==1:
            rtn[buckets-1]+=1
        rtn[int(data[i]*buckets)]+=1
    rtn2=[0]*buckets
    for i in range(buckets):
        rtn2[i]=float(rtn[i])/(rtn[i]+rtn[-i-1])
    print(rtn)
    print(rtn2)

def load1000():
    import pickle
    f=open('1000.2.pckl')
    rtn=pickle.load(f)
    f.close()
    return rtn

def cor(data,samples=200):
    import random as r
    rtn=[]
    txt=''
    for i in range(samples):
        n=data[int(len(data)*r.random())]
        if n[0]:
            txt+=str(n[0])+'\t'+str(n[2])+'\n'
            rtn.append([n[0],n[3]])
    print(txt)
    return rtn

def sheeple(data,samples=10000):
    import random as r
    sports=[]
    wp=[]
    for i in range(samples):
        n=data[int(len(data)*r.random())]
        if n[0] and n[2]:
            if not(n[2] in sports):
                sports.append(n[2])
                wp.append([0,0])
            if n[0]>0.5:
                wp[sports.index(n[2])][0]+=1.0
            wp[sports.index(n[2])][1]+=1
    txt=''
    for i in range(len(sports)):
        txt+=(sports[i]+'\t'+str(wp[i][0]/wp[i][1])+'\t'+str(wp[i][1])+'\n')
    print(txt)

def gameTypes(data,samples=500):
    import random as r
    gt=[]
    for i in range(samples):
        n=data[int(len(data)*r.random())][1]
        if n:
            n=n[n.find(':')+1:].lower()
            if not(n in gt):
                gt.append(n)
    print(gt)
        

a=load1000()
gameTypes(a)
