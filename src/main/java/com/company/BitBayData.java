package com.company;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import javax.json.*;


public class BitBayData extends BitData{

    public static final String BTC_USD = "https://bitbay.net/API/Public/BTC/orderbook.json";
    public static final String LTC_USD =  "https://bitbay.net/API/Public/LTC/orderbook.json";
    public static final String BTC_EUR = "https://bitbay.net/API/Public/BTCEUR/orderbook.json";
    public static final String BTC_ETH = "https://bitbay.net/API/Public/LTCEUR/orderbook.json";

    BitBayData(String title) {
        super(title, BTC_USD, LTC_USD, BTC_EUR, BTC_ETH);
    }

    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();


            JsonArray JBids = jsonObject.getJsonArray("bids");
            bids = convertToList(JBids);
            JsonArray JAsks = jsonObject.getJsonArray("asks");
            asks = convertToList(JAsks);

        }
    }

    @Override
    protected ArrayList<double[]> convertToList(JsonArray jarr) {
        ArrayList<double[]> arrayList = new ArrayList<>();
        String rateInString, amountInString;
        for (int i = 0; i < jarr.size(); i++) {
            rateInString = jarr.getJsonArray(i).get(0).toString();
            amountInString = jarr.getJsonArray(i).get(1).toString();
            arrayList.add(new double[]{convertStringToDouble(rateInString),
                    convertStringToDouble(amountInString)});
        }
        return arrayList;
    }
}