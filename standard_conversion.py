month = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
         '07':'Jul','08':'Aug','09':'Sept','10':'Oct','11':'Nov','12':'Dec'}

values = {'Date' : 'x', 'Time' : 'x', 'Latitude' :'x', 'Longitude' :'x',
          'Elevation' :'x', 'Ceiling' :'x', 'Visibility' :'x', 'MissVal' :'x', 'LatSide' : 'x', 'LonSide' : 'x'}

def Date_Time(a):
    DLine = a.split(',')
    DTG_D_T = DLine[1].split(' ')
    DSep = DTG_D_T[1].split('-')
    values['Date'] = DSep[2]+month[DSep[1]]+DSep[0]
    values['Time'] = DTG_D_T[2].strip()
    
def Latitude(a):
    LatLine = a.split(',')
    Lat_val= '%.5f' %float(LatLine[1])
    values['Latitude'] = Lat_val
    values['LatSide'] = LatLine[2].strip()
    
def Longitude(a):
    LonLine = a.split(',')
    Lon_val = '%.5f' %float(LonLine[1])
    values['Longitude'] = str(Lon_val)
    values['LonSide'] = LonLine[2].strip()

def Elevation(a):
    EleLine = a.split(',')
    Ele_val= '%.1f' %float(EleLine[1])
    values['Elevation'] = Ele_val

def Miss_Val(a):
    MissLine = a.split(',')
    values['MissVal'] = MissLine[1].strip()
    
def Ceiling(a):
    print("No Ceiling")

def Visibility(a):
    print("No Visibility")

Extract = {"DTG":Date_Time,"LAT":Latitude,"LON":Longitude,"ELEV":Elevation,
           "CEL":Ceiling,"VIS":Visibility,"MISSING":Miss_Val}

X=[]
L=[]
count = 0
serial = 0
virt = 0
dpt = 0

with open('FULL CSV 21.txt', 'r') as f:
    for line in f:
      if(line == "\n"):
          break 
      sp = line.split(",")
      try:
          Extract[sp[0]](line)
          count+=1
      except KeyError:
          count+=1
          continue
        
    for i in values:
        if(values[i]=='x'):
            values[i] = values['MissVal']
   
    f.seek(0)
    for k in range(count+3):
        next(f)
    
    lines=f.readlines()
    for i in lines:
        x = i.split(',')
        y = int(x[5])
        X.append(y)
    z = 0
    x = min(X, key=lambda x:abs(x-z))
##    print(x)
    L.append(x)
    z = 200
    x = min(X, key=lambda x:abs(x-z))
##    print(x)
    L.append(x)
    j = 500
    for i in range(9):
        x = min(X, key=lambda x:abs(x-j))
        j = j+500
##        print(x)
        L.append(x)
    j = 5000
    for i in range(18):
        x = min(X, key=lambda x:abs(x-j))
        j = j+1000
##        print(x)
        L.append(x)
##    print(L)
    
    data = open("standard.txt","w")
    data.write('Date: '+values['Date']+' Time: '+values['Time']+' Latitude: '+values['Latitude']+' Longitude: '
                 +values['Longitude']+'\nElevation: '+values['Elevation']+' Ceiling: '+values['Ceiling']+' Visibility: '+values['Visibility'])
    data.write('\n\nLine\tHeight\tWind Direction\tWind Speed\tVirt Temp\t\tPressure\t\tTemperature\n')
    data.write('\t(m)\t(tens of mils)\t(kt)\t\t(K*10)\t\t(mb)\t\t(K*10)\n')
    j=0
    for i in lines:
        s =i.split(',')
        if (int(s[5])==int(L[j])):
            Temp = float(s[1])
            Pres = float(s[0])
            Dpt = Temp-(100-int(s[2]))/5.0
            virt = int(((Temp+273.15)/(1-0.379*(6.11*10**((7.5*Dpt)/(237.7+Dpt)))/Pres))*10)
            Temp = '%.0f' %(round(Temp+273.15,1)*10)
            Pres = int(Pres)
            Wspeed = '%.0f' %float(s[4])
            data.write(str(serial)+'\t'+s[5].strip()+'\t'+s[3].strip()+'\t\t'+str(Wspeed)+'\t\t'+str(virt)+'\t\t'+str(Pres)+'\t\t'+str(Temp)+"\n")
            serial+=1
            j+=1
            if(j==len(L)):
                break
       
    data.close()
    f.close()

def InitialP():
    k = open("standard.txt","r")
    s = k.readline()
    while(s.split('\t')[0] != '0'):
        s = k.readline()
        continue
    k.close()
    s = s.split('\t')
    while '' in s : s.remove('')
    return s[5].strip()

def Octant(Latitude, LatSide, Longitude, LonSide):
    Latitude = float(Latitude)
    Longitude = float(Longitude)   
    if(Latitude == 'x' or Longitude == 'x' or LatSide == 'x' or LonSide == 'x'): return 9
    
    if(LatSide == 'N'):
        if(LonSide == 'W'):
            if(0 < Longitude < 90): return 0
            if(90 < Longitude < 180): return 1
        if(LonSide == 'E'):
            if(0 < Longitude < 90): return 3
            if(90 < Longitude < 180): return 2
    
    if(LatSide == 'S'):
        if(LonSide == 'W'):
            if(0 < Longitude < 90): return 5
            if(90 < Longitude < 180): return 6
        if(LonSide == 'E'):
            if(0 < Longitude < 90): return 8
            if(90 < Longitude < 180): return 7
    
Lat = str(round(float(values['Latitude'])*10)).zfill(3)
Lon = str(round(float(values['Longitude'])*10)).zfill(4)[1:]
T = values['Time'].split(':')
T = T[0]+T[1][0]
E = str(round(float(values['Elevation'])/10)).zfill(3)
D = values['Date'][0:2]
O = Octant(values['Latitude'], values['LatSide'], values['Longitude'], values['LonSide'])

def METCM():
    f = open("standard.txt","r")
    newf = open("metcm.txt","w")
    P = str(round(float(InitialP()))).zfill(4)[1:]
    newf.write("METCM"+str(O)+Lat+Lon+D+T+'0'+E+P+'\n')
    p = f.readline()
    while(p.split('\t')[0] != '0'):
        p = f.readline()
        continue

    def metcm_conv(x): 
        dat = x.split('\t')
        while '' in dat : dat.remove('')
        l = dat[0].zfill(2)
        Wd = dat[2].zfill(3)
        Ws = dat[3].zfill(3)
        Vt = dat[4].zfill(4)
        Pr = dat[5].zfill(4)
        newf.write(l+Wd+Ws+' '+Vt+Pr+'\n')

    metcm_conv(p)
    for line in f:
        metcm_conv(line)

    f.close()
    newf.close()


def METB2():
    f = open("standard.txt","r")
    newf = open("metb2.txt","w")
    P = str('%.1f' %(float(InitialP())*100/1013.25))
    newf.write("MEB2"+str(O)+Lat+Lon+D+T+'0'+E+P+'\n')
    p = f.readline()
    while(p.split('\t')[0] != '0'):
        p = f.readline()
        continue
    
    def TTT(Temp, Ele):
        Temp = (Temp/10)-273.15
        if(Ele > 11000):# and <25000
            surft = -56.5
        else:
            surft = 15-6.5*int(Ele/1000)
        TTT = abs(round((Temp*100/surft)*10))
        return str(TTT).zfill(4)[1:]         

    def DDD(Pres, Temp): #Surface Density percentage
        Temp = Temp/10
        R = 0.0209521*0.001
        DDD = round((Pres/(R*Temp*28.97))*100/1225)
        return str(DDD).zfill(4)[1:]
    
    def WindSpeed(W):
        if(W<100):
            return str(W).zfill(2), 0
        else:
            return str(W-100).zfill(2), 80
        
    def metb2_conv(x):
        dat = x.split('\t')
        while '' in dat: dat.remove('')
        l = dat[0].zfill(2)
        Wd = str(round(float(dat[2])/10)).zfill(2)
        Ws, off  = WindSpeed(int(dat[3]))
        print(Ws)
        TT = TTT(float(dat[6]), float(dat[1]))
        DD = DDD(float(dat[5]), float(dat[6])) #Pres, Temp
        l = str(int(l)+off).zfill(2)
        newf.write(l+' '+Wd+' '+Ws+' '+TT+' '+DD+'\n')
        
        
    metb2_conv(p)
    for line in f:
        metb2_conv(line)

    f.close()
    newf.close()
    
##def METTA():
##    f = open("standard.txt","r")
##    newf = open("metta.txt","w")
##    newf.write("META"+str(O)+Lat+Lon+D+T+'0'+E+P+'\n')
##    p = f.readline()
##    while(p.split('\t')[0] != '0'):
##        p = f.readline()
##        continue
##    def metta_conv(x):
##        dat = x.split('\t')
##        while '' in dat: dat.remove('')
##        
##
##    metta_conv(p)
##    for line in f:
##        metta_conv(line)
##
##    f.close()
##    newf.close()
    
def METFM():
    f = open("standard.txt","r")
    newf = open("metfm.txt","w")
    newf.write("METFM"+str(O)+Lat+Lon+D+T+'0'+E+P+'\n')
    p = f.readline()
    while(p.split('\t')[0] != '0'):
        p = f.readline()
        continue
    def metfm_conv(x):
        dat = x.split('\t')
        while '' in dat: dat.remove('')
        l = dat[0].zfill(2)
        Wd = dat[2].zfill(3)
        Ws = dat[3].zfill(3)
        newf.write(l+Wd+Ws+'\n')

    metfm_conv(p)
    for line in f:
        metfm_conv(line)

    f.close()
    newf.close()


METB2()
METTA()
METCM()
METFM()


