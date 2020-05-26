import requests
import csv
from appJar import gui
import time

class Calculator:
    def __init__(self,filename,basecurency):
        self.filename=filename
        self.array=[]
        self.primaryURL="https://api.bitbay.net/rest/trading/transactions/"
        self.secondaryURL="https://api.bittrex.com/v3/markets/"
        self.basecur=basecurency.upper()
        self.round=0

    def addCurr(self,ammount,name):
        isInside=False
        for el in self.array:
            if name.upper()==el[0]:
                return 0
          
        response=requests.get(self.primaryURL+name.upper()+"-"+self.basecur).json()
        if response['status']=="Ok" and len(response['items'])>0:
            tup=(name.upper(),ammount,1)
            self.array.append(tup)
            return 1
        response=requests.get(self.secondaryURL+name.upper()+"-"+self.basecur+"/trades").json()
        if len(response[0])==5:
            tup=(name.upper(),ammount,2)
            self.array.append(tup)
            return 1
        else:
            return 0
            
                    
    def countProvision(self,val):
        self.round=self.round+val
        if self.round>=975000:
            return 0.23
        else:
            drop=self.round//1250
            return (0.0043-drop/10000)*val
        
        
    def delCurr(self, name):
        for el in self.array:
            if el[0]==name.upper():
                self.array.remove(el)
                return 1
        return 0

    def editCurr(self, name, newval):
        for el in self.array:
            if el[0]==name.upper():
                self.delCurr(name)
                self.addCurr(float(newval), name)
                return 1
        return 0

    def findVal(self, name, val):
        response=requests.get(self.primaryURL+name.upper()+"-"+self.basecur+"?limit=299").json()
        acc=[]
        for el in response["items"]:
            if el["ty"]=="Buy" and float(el["a"])<=val:
                tup=(float(el["a"]),float(el["r"]))
                acc.append(tup)
        return self.helpCounter(acc, val)
    
    def findVal2(self, name, val):
        def take(elem):
            return elem[0]*elem[1]
        response=requests.get(self.secondaryURL+name.upper()+"-"+self.basecur+"/trades").json()
        acc=[]
        for el in response:
            if el['takerSide']=="BUY":
                tup=(float(el['quantity']), float(el["rate"]))
                acc.append(tup)
        return self.helpCounter(acc,val)
                
        
    def helpCounter(self,acc,val):
        def take(elem):
            return elem[0]*elem[1]
        acc.sort(key=take, reverse=True)
        cash=0
        ammount=val
        for el in acc:
            if ammount-el[0]>=0:
                ammount=ammount-el[0]
                transaction=el[0]*el[1]
                cash=cash-self.countProvision(transaction)+transaction
        cash=cash+cash/(val-ammount)*ammount
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
            if el[2]==1:
                suma=suma+self.findVal(el[0],el[1])
            else:
                suma=suma+self.findVal2(el[0],el[1])
        self.round=0
        return suma
    
    def simpleArr(self):
        acc=[]
        for el in self.array:
            acc.append(el[0])
        return acc

    def findSimpleVal(self,name):
        for el in self.array:
            if el[0]==name.upper():
                acc=el
                break
        if acc[2]==1:
            cash=self.findVal(acc[0],acc[1])
        if acc[2]==0:
            cash=self.findVal2(acc[0],acc[1])
        self.round=0
        return str(acc[1])+" "+str(acc[0])+" is worth "+str(round(cash,2))+" USD"
    def start(self):
       
        def pressMenu(button):
            if button=="Add":
                app.showSubWindow("Adding")
            
            if button=="Delete":
                app.showSubWindow("Deleting")
            if button=="Close":
                app.stop()
            if button=="Count Value":
                app.infoBox("SUM", str(round(self.findSum(),2))+" "+self.basecur, parent=None)

            if button=="Edit asset":
                app.showSubWindow("Editing")
                
                
                
        def pressAdd(button):
            if button=="Confirm":
                cur=app.getEntry("Currency")
                val=app.getEntry("Ammount")
                app.clearEntry("Currency")
                app.clearEntry("Ammount")
                if self.addCurr(float(val),cur)==1:
                    app.addMenuItem("Wallet", cur.upper(), wall, shortcut=None, underline=-1)
                    self.addCurr(float(val),cur)
                else:
                    app.infoBox("ERROR1", "Sorry we don't have these asset or you have already add it", parent=None)
                app.clearEntry("Ammount")
                app.clearEntry("Currency")
                app.hideSubWindow("Adding")
        def pressDel(button):
            if button=="Approve":
                cur=app.getEntry("Currency to del")
                if self.delCurr(cur)==1:
                    try:
                        app.deleteMenuItem("Wallet", cur.upper())
                    except:
                        print("")
                else :
                    app.infoBox("ERROR2", "Your asset is already removed", parent=None)
                    self.delCurr(cur)
                app.clearEntry("Currency to del")
                app.hideSubWindow("Deleting")

        def pressEdit(button):
            if button=="Change":
                cur=app.getEntry("Currency to edit")
                val=app.getEntry("New ammount")
                if self.editCurr(cur.upper(), val)==0:
                    app.infoBox("ERROR3", "Nothing to edit, maybe try add new currency", parent=None)
                else:
                    try:
                        self.editCurr(cur, val)
                    except:
                        print("")
                app.clearEntry("Currency to edit")
                app.clearEntry("New ammount")
                app.hideSubWindow("Editing")
        def wall(button):
            app.infoBox("Cur",str(self.findSimpleVal(button)), parent=None)
            
            
        app = gui("Calculator", "400x200")
        app.addLabel("title", "Welcome to Calculator")
        app.setBg("light green")
        app.setLabelBg("title", "green")
        app.addButtons(["Add", "Delete","Edit asset","Count Value","Close"],pressMenu)
        app.startSubWindow("Adding",modal=True)
        app.addLabelEntry("Currency")
        app.addLabelEntry("Ammount")
        app.addButtons(["Confirm"],pressAdd)
        app.startSubWindow("Deleting",modal=True)
        app.addLabelEntry("Currency to del")
        app.addButtons(["Approve"],pressDel)
        app.startSubWindow("Editing",modal=False)
        app.addLabelEntry("Currency to edit")
        app.addLabelEntry("New ammount")
        app.addButtons(["Change"],pressEdit)
        app.createMenu("Wallet")
        app.addMenuList("Wallet", self.simpleArr(), wall)
            
        
        app.go()

cal=Calculator("archive.csv","USD")

cal.loadArchive()


cal.start()
cal.createArchive()


