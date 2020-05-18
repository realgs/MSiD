const proxyurl = "https://cors-anywhere.herokuapp.com/";
const urlMarkets = 'https://api.bittrex.com/api/v1.1/public/getmarkets';


const getMarkets = async () => {
    const response  = await fetch(
        proxyurl+urlMarkets,
      {
        method: 'GET'
      }
    );
     const data = await response.json();
    
    if(data.success) {
      return data.result.map(function(elem) {
        return {
          BaseCurrency: elem.BaseCurrency,
          MarketCurrency: elem.MarketCurrency,
          MarketName: elem.MarketName
        }
      });
    }
    else return data.message;
      
  }

 const getOrders = async (symbol,type) => {
  const response = await fetch(
        proxyurl+`https://api.bittrex.com/api/v1.1/public/getorderbook?market=${symbol}&type=${type}`,
      {
        method: 'GET'
      }
    )
    const data = await response.json();

    return data;
  }

  export {getMarkets, getOrders};