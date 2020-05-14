import requests
import math 
import mysql.connector
url="http://api.nbp.pl/api/cenyzlota/2020-01-01/2020-03-31/?format=json"
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="mydatabase"
)
mycursor = mydb.cursor()
current_calibration=(0,0)
def freshStart():
    mycursor.execute("DROP TABLE zloto")
    mycursor.execute("CREATE TABLE zloto (date VARCHAR(20), val VARCHAR(10))")

def loadVals():
    workin_url="http://api.nbp.pl/api/cenyzlota/20"
    year=13
    while year<20:
        for i in range (1,12):
            if i<9:
                response=requests.get(workin_url+str(year)+"-0"+str(i)+"-01/20"+str(year)+"-0"+str(i+1)+"-01/?format=json").json()
            if i==9:
                response=requests.get(workin_url+str(year)+"-0"+str(i)+"-01/20"+str(year)+"-1"+str(i-9)+"-01/?format=json").json()
            if i==10:
                response=requests.get(workin_url+str(year)+"-1"+str(i-10)+"-01/20"+str(year)+"-1"+str(i-9)+"-01/?format=json").json()
            if i==11:
                response=requests.get(workin_url+str(year)+"-1"+str(2)+"-01/20"+str(year+1)+"-01-01/?format=json").json()
            for el in response:
                tup=(el["data"], el["cena"])
                #print(tup)
                sql = "INSERT INTO zloto (date, val) VALUES (%s, %s)"
                mycursor.execute(sql, tup)
                mydb.commit()
        year=year+1

def getVals():
    mycursor.execute("SELECT val FROM zloto")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(float(x[0]))
def countEstym(array):
    i=0
    s=0
    est=0
    
    for x in array:
        s=s+float(x[0])
        i=i+1
    if i!=0:
        s=s/i
        for x in myresult:
            est=est+(float(x[0])-s)
        
        est=est/i
        
        math.sqrt(est)
        print(est)
        
    else:
        print("Empty database")
    
def findVal(ammount,time,percentage_drop):
    zloty=0
    gold=0
    it=0
    end_val=0
    dataLoaded=False
    array=[]
    mycursor.execute("SELECT val FROM zloto")
    myresult = mycursor.fetchall()
    gold=ammount/float(myresult[0][0])
    for x in myresult:
        if dataLoaded==True:
            average=0
            for el in array:
                average=average+el
            average=average/time
            if zloty==0:
                if array[time-1]-average<0 and -1*(array[time-1]-average)/average>percentage_drop:
                    zloty=gold*float(x[0])
                    gold=0
            if gold==0:
                if array[time-1]-average>0:
                    gold=zloty/float(x[0])
                    zloty=0
            array.pop(0)
            array.append(float(x[0]))
        if dataLoaded==False:
            array.append(float(x[0]))
            if len(array)==time:
                dataLoaded=True
    
    end_val=zloty+gold*float(myresult[len(myresult)-1][0])
    return end_val
    
def calibrate(ammount):
    calibrated=(0,0,0)
    for it1 in range (2,31):
        percent=0.01
        for it2 in range (0,50):
            val=findVal(ammount,it1,percent)
            if val>calibrated[0]:
                calibrated=(val,it1,percent)
                percent=percent+0.01
                
    return (calibrated[1], calibrated[2])
def threeMonthSymulated(ammount):
    zloty=0
    gold=0
    symulation=[]
    isFull=False
    mycursor.execute("SELECT val FROM zloto")
    myresult = mycursor.fetchall()
    calibration=calibrate(ammount)
    #calibration=(5,0.01)
    work_array=[]
    
    response=requests.get(url).json()
    gold=ammount/float(response[0]["cena"])
    it=0
    for el in response:
        tup=(el["data"], el["cena"])
        symulation.append(tup)
        average=0
        if isFull==True:
            for x in work_array:
                average=average+x
            average=average/calibration[0]
            if zloty==0:
                if work_array[calibration[0]-1]-average<0 and -1*(work_array[calibration[0]-1]-average)/average>calibration[1]:
                    print ("sprzedaję złoto")
                    zloty=gold*float(el["cena"])
                    gold=0
            if gold==0:
                if work_array[calibration[0]-1]-average>0:
                    print ("kupuję złoto")
                    gold=zloty/float(el["cena"])
                    zloty=0
            work_array.append(float(el["cena"]))
            work_array.pop(0)
            
        if isFull==False:
            work_array.append(float(el["cena"]))
            if len(work_array)==calibration[0]:
                isFull=True
            
        it=it+1
        if it==30:
            for cur in symulation:
                sql = "INSERT INTO zloto (date, val) VALUES (%s, %s)"
                mycursor.execute(sql, cur)
                mydb.commit()
            calibration=calibrate(zloty+gold*float(work_array[calibration[0]-1]))
            work_array.clear()
            for it in range (len(symulation)-1,len(symulation)-(calibration[0]+1),-1):
                work_array.append(symulation[it][1])
            symulation.clear()
    
    print(gold)
    print(zloty+gold*response[len(response)-1]["cena"])
    
    
freshStart()         
loadVals()

threeMonthSymulated(1000)