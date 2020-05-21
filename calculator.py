import requests
import csv
from appJar import gui
import time

class Calculator:
    def __init__(self,filename,basecurency):
        self.filename=filename
        self.array=[]
        self.primaryURL="https://api.bitbay.net/rest/trading/transactions/"
        self.secondaryURL="https://api.gemini.com/v1"
        self.basecur=basecurency.upper()
        self.round=0

    def addCurr(self,ammount,name):
        isInside=False
        for el in self.array:
            if name.upper()==el[0]:
                isInside=True
        if isInside==False:    
            response=requests.get(self.primaryURL+name.upper()+"-"+self.basecur).json()
            if response['status']=="Ok":
                tup=(name.upper(),ammount,1)
                self.array.append(tup)
            else:
                response=requests.get(self.primaryURL+name.lower()+self.basecur.lower()).json()
                if response["timestamp"] is not None:
                    tup=(name.upper(),ammount,2)
    def countProvision(self,val):
        self.round=self.round+val
        if self.round>=975000:
            return 0.23
        else:
            drop=self.round//1250
            return 0.57+drop/100
        
        
    def delCurr(self, name):
        for el in self.array:
            if el[0]==name.upper():
                self.array.remove(el)

    def editCurr(self, name, newval):
        for el in self.array:
            if el[0]==name.upper():
                el[1]=newval

    def findVal(self, name, val):
        def take(elem):
            return elem[0]*elem[1]*0,75
        response=requests.get(self.primaryURL+name.upper()+"-"+self.basecur+"?limit=299").json()
        acc=[]
        ammount=val
        for el in response["items"]:
            if el["ty"]=="Buy" and float(el["a"])<=val:
                tup=(float(el["a"]),float(el["r"]))
                acc.append(tup)
        acc.sort(key=take, reverse=True)
        cash=0
        
        for el in acc:
            if ammount-el[0]>=0:
                ammount=ammount-el[0]
                transaction=el[0]*el[1]
                cash=cash+self.countProvision(transaction)*transaction
        
        return cash

    def createArchive(self):
        try:
            file=open(self.filename, "w", newline='')
            filewriter=csv.writer(file)
            filewriter.writerows(self.array)
            file.close()
        except:
            print ("Archive wasn't created")

    def loadArchive(self):
        try:
            file=open(self.filename, "r")
            data=csv.reader(file)
            for row in data:
                tup=(row[0],float(row[1]),float(row[2]))
                self.array.append(tup)
            file.close()
        except:
            print ("Archive wasn't created")
        
    def printArray(self):
        
        for el in self.array:
            print (el)

    def findSum(self):
        suma=0
        for el in self.array:
            if el[2]!=2:
                suma=suma+self.findVal(el[0],el[1])
        self.round=0
        return suma

        
    def start(self):
       
        def pressMenu(button):
            if button=="Add":
                app.showSubWindow("Adding")
            
            if button=="Delete":
                app.showSubWindow("Deleting")
            if button=="Close":
                app.stop()
            if button=="Count Value":
                app.infoBox("SUM", str(self.findSum())+" "+self.basecur, parent=None)
                
                
                
        def pressAdd(button):
            if button=="Confirm":
                cur=app.getEntry("Currency")
                val=app.getEntry("Ammount")
                app.clearEntry("Currency")
                app.clearEntry("Ammount")
                self.addCurr(float(val),cur)
                app.hideSubWindow("Adding")
        def pressDel(button):
            if button=="Approve":
                cur=app.getEntry("Currency to del")
                self.delCurr(cur)
                app.clearEntry("Currency to del")
                app.hideSubWindow("Deleting")
            
            
        app = gui("Calculator", "400x200")
        app.addLabel("title", "Welcome to Calculator")
        app.setBg("light green")
        app.setLabelBg("title", "green")
        app.addButtons(["Add", "Delete","Close","Count Value"],pressMenu)
        app.startSubWindow("Adding",modal=True)
        app.addLabelEntry("Currency")
        app.addLabelEntry("Ammount")
        app.addButtons(["Confirm"],pressAdd)
        app.startSubWindow("Deleting",modal=True)
        app.addLabelEntry("Currency to del")
        app.addButtons(["Approve"],pressDel)
        
        app.go()

cal=Calculator("archive.csv","USD")

cal.loadArchive()


cal.start()
cal.createArchive()


