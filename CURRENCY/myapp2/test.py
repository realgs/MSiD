import requests


urlGEMINI = "https://api.gemini.com/v1/book"
urlBITBAY= "https://bitbay.net/API/Public"
urlBITTREX= "https://api.bittrex.com/api/v1.1/public/getorderbook?market="
urlBITFINEX="https://api-pub.bitfinex.com/v2/book/"
geminiCURR=["/btcusd","/ltcbtc", "/ethbtc", "/ltcusd"]
bitbayCURR=["/BTCUSD/orderbook.json", "/LTCBTC/orderbook.json", "/ETHBTC/orderbook.json", "/LTCUSD/orderbook.json"]
bittrexCURR=["USD-BTC&type=both","BTC-LTC&type=both","BTC-ETH&type=both", "USD-LTC&type=both"]
bitfinexCURR=["tBTCUSD/R0", "tLTCBTC/R0", "tETHBTC/R0", "tLTCUSD/R0"]

def loadResponse(url,name, number):
    response=requests.get(url+name[number]).json()
    return response

def separateGEM(j,bidORask):
    defult_list=[]
    for el in j[bidORask]:
        tup=(float(el["amount"]),float(el["price"])/float(el["amount"]))
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

def countArbitration(listBuy,listSell):
    bestDeal=-10000.00
    for buy in listBuy:
        for sell in listSell:
            if float(buy[1])<=float(sell[1]) and float(buy[0])>=float(sell[0]) :
                val=(float(sell[1])-float(buy[1]))*float(sell[0])
                if bestDeal<val:
                    bestDeal=val
                    usedVals=(sell[0],buy[0],sell[1],buy[1],bestDeal)
                    
    return usedVals
                
            
def findCycle(number):
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
    buy=[geminiBid, bitbayBid, bitfinexBid]
    sell=[geminiAsk, bitbayAsk, bitfinexAsk]
    
    maximum=(0.0,0.0,0.0,0.0,0.0)
    for el1 in buy:
        for el2 in sell:
            val=countArbitration(el1,el2)
            print(val)
            if maximum[4]<=val[4]:
                maximum=val
    maxVal=maximum[4]           
    if number==1 or number==3:
        maxVal=maxVal*0.75
        
    else:
        maxVal=maxVal*0.99
        
  
    return maxVal   
    
    
def countAllCurrency():
    profitList=[]
    for i in range (0,4):
        profitList.append(findCycle(i))
    max=-1000.00
    for el in profitList:
        if max<el:
            max=el
            
    print(max)
    
    

#print(loadResponse(urlBITBAY,bitbayCURR, 0))
countAllCurrency()
   #asks kupuję bid sprzedaję do poprawy jutro 

    

    