package com.company;

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException, InterruptedException {
        BittrexData  bittrex = new BittrexData("bittrex");
        BitBayData  bitbay = new BitBayData("bitbay");
        CexData cex = new CexData("cex");
        HitbtcData hitbtc = new HitbtcData("hitbtc");
        CurrencyExchange observer = new CurrencyExchange();

        observer.addMarket(bittrex);
        observer.addMarket(bitbay);
        observer.addMarket(cex);
        observer.addMarket(hitbtc);


        bitbay.getDataBTCUSD();
        bitbay.printDiff(10);

        bittrex.getDataBTCUSD();
        bittrex.printDiff(10);

        cex.getDataBTCUSD();
        cex.printDiff(10);

        hitbtc.getDataBTCUSD();
        hitbtc.printDiff(10);

        observer.run();


    }
}
