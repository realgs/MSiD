package com.company;

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException, InterruptedException {
        BittrexData  bittrex = new BittrexData("bittrex");
        BitBayData  bitbay = new BitBayData("bitbay");
        CexData cex = new CexData("cex");
        HitbtcData hitbtc = new HitbtcData("hitbtc");
        VirtualBudget account = new VirtualBudget(1000, 1000);
        CurrencyExchange observer = new CurrencyExchange(account);

        observer.addMarket(bittrex);
        observer.addMarket(bitbay);
        observer.addMarket(cex);
        observer.addMarket(hitbtc);


        bitbay.getDataBTCEUR();
        bitbay.printDiff(10);

        bittrex.getDataBTCEUR();
        bittrex.printDiff(10);

        cex.getDataBTCEUR();
        cex.printDiff(10);

        hitbtc.getDataBTCEUR();
        hitbtc.printDiff(10);

        observer.run();


    }
}
