package com.company;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

public class CurrencyExchange {

    public static final int BTC_USD=1, BTC_EUR=2, LTC_USD=3, LTC_EUR=4;

    ArrayList<BitData> markets = new ArrayList<>();

    public void run() throws InterruptedException, IOException {
        if(markets.size()>0){
            while(true) {
                System.out.println("Fetch data. Time: " + LocalDateTime.now());
                exchangeObserver(BTC_USD);
                exchangeObserver(BTC_EUR);
                exchangeObserver(LTC_USD);
                exchangeObserver(LTC_EUR);
                TimeUnit.SECONDS.sleep(10);
            }
        }
    }



    public void addMarket(BitData newMarket){
        markets.add(newMarket);
    }

    private void exchangeObserver(int option) throws IOException, InterruptedException {
        double bestAskPrice=Double.MAX_VALUE, bestBidPrice=-1.0, bestAskAmount=0.0, bestBidAmount=0.0;
        int marketIdAsk=-1, marketIdBid=-1;
        double[] currentMarket;
        boolean success;
        for(int i=0; i<markets.size(); i++) {

            success = getData(option, i);


            if(success){
                currentMarket = markets.get(i).getBestAsk();

                if(bestAskPrice>currentMarket[0]) {
                    bestAskPrice = currentMarket[0];
                    bestAskAmount = currentMarket[1];
                    marketIdAsk = i;
                }

                currentMarket = markets.get(i).getBestBid();

                if(bestBidPrice<currentMarket[0]) {
                    bestBidPrice = currentMarket[0];
                    bestBidAmount = currentMarket[1];
                    marketIdBid = i;
                }
            }
        }
        if(bestAskPrice<bestBidPrice) {
            arbitrage(option, bestAskPrice, bestBidPrice, bestAskAmount, bestBidAmount, marketIdAsk, marketIdBid);
        }
    }

    private boolean getData(int option, int marketId) throws IOException, InterruptedException {
        boolean success = false;
        switch (option) {
            case BTC_USD:
                success = markets.get(marketId).getDataBTCUSD();
                break;
            case BTC_EUR:
                success = markets.get(marketId).getDataBTCEUR();
                break;
            case LTC_USD:
                success = markets.get(marketId).getDataLTCUSD();
                break;
            case LTC_EUR:
                success = markets.get(marketId).getDataLTCEUR();
                break;
            default:
                return success;

        }
        return success;
    }

    private void arbitrage(int option, double bestAskPrice, double bestBidPrice,
                           double askAmount, double bidAmount, int askMarketId, int bidMarketId) {
        double amount = Math.min(askAmount,bidAmount);
        double gain = (bestBidPrice - bestAskPrice) * amount;
        switch (option) {
            case BTC_USD:
                System.out.printf("On market %s buy %.2fBTC at the exchange rate: %.2f sell on market %s at the exchange rate: %.2f, gain: %.2fUSD \n",
                        markets.get(askMarketId).getTitle(), amount, bestAskPrice, markets.get(bidMarketId).getTitle(),
                        bestBidPrice, gain);
                break;
            case BTC_EUR:
                System.out.printf("On market %s buy %.2fBTC at the exchange rate: %.2f sell on market %s at the exchange rate: %.2f, gain: %.2fEUR \n",
                        markets.get(askMarketId).getTitle(), amount, bestAskPrice, markets.get(bidMarketId).getTitle(),
                        bestBidPrice, gain);
                break;
            case LTC_USD:
                System.out.printf("On market %s buy %.2fLTC at the exchange rate: %.2f sell on market %s at the exchange rate: %.2f, gain: %.2fUSD \n",
                        markets.get(askMarketId).getTitle(), amount, bestAskPrice, markets.get(bidMarketId).getTitle(),
                        bestBidPrice, gain);
                break;
            case LTC_EUR:
                System.out.printf("On market %s buy %.2fLTC at the exchange rate: %.2f sell on market %s at the exchange rate: %.2f, gain: %.2fEUR \n",
                        markets.get(askMarketId).getTitle(), amount, bestAskPrice, markets.get(bidMarketId).getTitle(),
                        bestBidPrice, gain);
                break;
            default:
                return;

        }


    }



}
