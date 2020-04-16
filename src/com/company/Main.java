package com.company;

import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        BitBayData  bitcoinTrade = new BitBayData();
        try {
            bitcoinTrade.analysisDate(10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
