package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

public class HitbtcData extends BitData {

    public static final String BTC_USD = "https://api.hitbtc.com/api/2/public/orderbook/BTCUSD";
    public static final String LTC_USD = "https://api.hitbtc.com/api/2/public/orderbook/LTCUSD";
    public static final String BTC_EUR = "https://api.hitbtc.com/api/2/public/orderbook/BTCEURS";
    public static final String BTC_ETH = "https://api.hitbtc.com/api/2/public/orderbook/LTCEURS";
    public static final double FEE = 0.002;

    HitbtcData(String title) {
        super(title, BTC_USD, LTC_USD, BTC_EUR, BTC_ETH, FEE);
    }

    @Override
    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();


            JsonArray JBids = jsonObject.getJsonArray("bid");
            bids = convertToList(JBids);
            JsonArray JAsks = jsonObject.getJsonArray("ask");
            asks = convertToList(JAsks);

        }
    }

    @Override
    protected ArrayList<double[]> convertToList(JsonArray jarr) {
        ArrayList<double[]> arrayList = new ArrayList<>();
        String rateString, amountString;
        for (int i = 0; i < jarr.size(); i++) {
            rateString = jarr.getJsonObject(i).get("price").toString();
            amountString = jarr.getJsonObject(i).get("size").toString();
            arrayList.add(new double[]{convertStringToDouble(rateString),
                    convertStringToDouble(amountString)});

        }
        return arrayList;
    }
}
