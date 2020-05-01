package com.company;

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException, InterruptedException {
        BittrexData  bittrex = new BittrexData("bittrex");
        BitBayData  bitbay = new BitBayData("bitbay");
        CexData cex = new CexData("cex");
        BitstampData bitstamp = new BitstampData("bitstamp");

        bitbay.getData("https://bitbay.net/API/Public/BTC/orderbook.json");
        bitbay.printDiff(10);

        bittrex.getData("https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both");
        bittrex.printDiff(10);

        cex.getData("https://cex.io/api/order_book/BTC/USD/");
        cex.printDiff(10);

        bitstamp.getData("https://www.bitstamp.net/api/order_book/btcusd");
        bitstamp.printDiff(10);


    }
}
