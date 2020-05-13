import requests


urlGEMINI = "https://api.gemini.com/v1/book"
urlBITBAY= "https://bitbay.net/API/Public"
urlBITTREX= "https://api.bittrex.com/api/v1.1/public/getorderbook?market="
urlBITFINEX="https://api-pub.bitfinex.com/v2/book/"
geminiCURR=["/btcusd","/ltcbtc", "/ethbtc", "/ltcusd"]
bitbayCURR=["/BTCUSD/orderbook.json", "/LTCBTC/orderbook.json", "/ETHBTC/orderbook.json", "/LTCUSD/orderbook.json"]
bittrexCURR=["USD-BTC&type=both","BTC-LTC&type=both","BTC-ETH&type=both", "USD-LTC&type=both"]
bitfinexCURR=["tBTCUSD/R0", "tLTCBTC/R0", "tETHBTC/R0", "tLTCUSD/R0"]
bankAccount=[]
def loadResponse(url,name, number):
    response=requests.get(url+name[number]).json()
    return response

def separateGEM(j,bidORask):
    defult_list=[]
    for el in j[bidORask]:
        tup=(float(el["amount"]),float(el["price"]))
        defult_list.append(tup)
    return defult_list

def seperateBITB(j,bidORask):
    defult_list=[]
    for el in j[bidORask]:
        tup=(float(el[1]), float(el[0]))
        defult_list.append(tup)
    return defult_list

def separateBITT(j,buyORsell):
    defult_list=[]
    for el in j["result"][buyORsell]:
        tup=(el["Quantity"],el["Rate"])
        defult_list.append(tup)
    return defult_list
def separateBITF(j,bidOrask):
    defult_list=[]
    if bidOrask=="kids":
        for el in j:
            if float(el[1])*float(el[2])>0:
                tup=(float(el[2]), float(el[1]))
                defult_list.append(tup)
        return defult_list
    else:
        for el in j:
            if float(el[1])*float(el[2])<0:
                tup=(float(el[2])*-1, float(el[1]))
                defult_list.append(tup)
        return defult_list

def countArbitration(listSell,listBuy, curr1, curr2):
    bestDeal=-10000.00
    val=0.0
    action=[0.0, 0.0, 0.0,]
    for buy in listBuy:
        for sell in listSell:
            if float(buy[1])<=float(sell[1]) and float(buy[0])>=float(sell[0]) and bankAccount[curr1]>buy[0]*buy[1] :
                val=(float(sell[1])-float(buy[1]))*float(sell[0])
                if bestDeal<val:
                    bestDeal=val
                    action[0]=bankAccount[curr1]-buy[0]*buy[1]+sell[0]*sell[1]
                    action[1]=bankAccount[curr2]+buy[0]-sell[0]
                    action[2]=bestDeal
    return action
                
            
def findCycle(number, cur1,cur2):
    responseGemini=loadResponse(urlGEMINI, geminiCURR,number)
    responseBitbay=loadResponse(urlBITBAY, bitbayCURR,number)
    responseBittrex=loadResponse(urlBITTREX, bittrexCURR,number)
    responseBitfinex=loadResponse(urlBITFINEX, bitfinexCURR,number)
    geminiBid=separateGEM(responseGemini,"bids")
    geminiAsk=separateGEM(responseGemini,"asks")
    bitbayBid=seperateBITB(responseBitbay, "bids")
    bitbayAsk=seperateBITB(responseBitbay, "asks")
    bittrexBid=separateBITT(responseBittrex, "buy")
    bittrexAsk=separateBITT(responseBittrex, "sell")
    bitfinexBid=separateBITF(responseBitfinex, "bids")
    bitfinexAsk=separateBITF(responseBitfinex, "asks")
    buy=[ geminiBid, bitbayBid, bittrexBid, bitfinexBid]
    sell=[ geminiAsk, bitbayAsk,bittrexAsk, bitfinexAsk]
    
    
    
    maximum=0.0
    action=[0.0, 0.0, 0.0, cur1, cur2]
    for el1 in buy:
        for el2 in sell:
            val=countArbitration(el1,el2,cur1,cur2)
            if action[2]<=val[2]:
                for i in range (0,3):
                    action[i]=val[i]
          
    if number==0 or number==3:
        action[2]=action[2]*0.5
        
    else:
        action[2]=action[2]*0.99
        
  
    return action 
    
    
def countAllCurrency():

    profitList=[]
    for i in range (0,3):
        if i==0:
            profitList.append(findCycle(i, 0, 1))
        if i==1:
            profitList.append(findCycle(i, 2, 1))
        if i==2:
            profitList.append(findCycle(i, 1, 3))
        if i==3:
            profitList.append(findCycle(i, 0, 2))
        

    
    action=[0.0, 0.0, 0.0, 0, 0]
    for el in profitList:
        if action[2]<=el[2]:
            action=el
                
    if action[2]>0.0:
        bankAccount[action[3]]=action[0]
        bankAccount[action[4]]=action[1]
        
    

def startFund(usd, btc, ltc, eth):
    bankAccount.append(usd)
    bankAccount.append(btc)
    bankAccount.append(ltc)
    bankAccount.append(eth)

def printCash():
    print ("bank account")
    for el in bankAccount:
        print("%.2f" %el)


startFund(10000.00, 1.00, 1000.00, 500)
for i in range (0,10):
    countAllCurrency()
printCash()
   

    

    
