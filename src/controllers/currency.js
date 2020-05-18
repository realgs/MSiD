import {getOrders} from '../Api/bittrex'

const getSymbol = (listCurrency, resourcesCurrency, convertCurrency) => {
    let res = listCurrency.find((elem) => elem.BaseCurrency === convertCurrency &&  elem.MarketCurrency === resourcesCurrency);
    if(res) {
        return {...res, type:"buy"};
    }
    
    res = listCurrency.find((elem) => elem.MarketCurrency === convertCurrency && elem.BaseCurrency === resourcesCurrency);
    if(res) {
        return {...res, type:"sell"};
    }
    console.log(resourcesCurrency+" "+convertCurrency);
    return {
        BaseCurrency: convertCurrency,
        MarketCurrency: resourcesCurrency,
        MarketName: ""};
}

const convertCurrency = async (symbol, type, amount, id) => {
    const res = await getOrders(symbol, type)
    const arr = res.result;
    console.log(arr);
    let i = 0, tmp_amount=0, sum=0;
        if(type==='buy'){
            while (i<arr.length && amount-tmp_amount>arr[i].Quantity) {
                sum += arr[i].Quantity*arr[i].Rate;
                tmp_amount +=  arr[i].Quantity
                i++;
            }
        } 
        else if(type==='sell'){
            while (i<arr.length && amount-tmp_amount>arr[i].Rate*arr[i].Quantity) {
                console.log(i);
                sum+=arr[i].Quantity;
                tmp_amount +=  arr[i].Quantity*arr[i].Rate;
                i++;
            }
        }
        return {id: id, symbol: symbol, amount:sum}
}

const convertList = (resources, listSymbols, base) => {
    const arr = resources.map((elem) => convertElem(listSymbols, base, elem))
    return arr
}

const convertElem = async (listSymbols, base, elem) => {
    if(base===elem.symbol) return {id: elem.id, symbol:base+"-"+elem.symbol, amount:elem.amount, status:"success"}
    const market = getSymbol(listSymbols, elem.symbol, base);
    console.log(market);
    if(!market.MarketName) return {id: elem.id, symbol: "", status:"no data"}
    const res = await convertCurrency(market.MarketName, market.type, elem.amount, elem.id);
    console.log(res);
    return {...res, status:"success"}
}

export {getSymbol, convertCurrency, convertList};