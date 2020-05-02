package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

public class BittrexData extends BitData{

    public static final String BTC_USD = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both";
    public static final String LTC_USD = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-LTC&type=both";
    public static final String BTC_EUR = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=EUR-BTC&type=both";
    public static final String LTC_EUR = "";
    public static final double FEE = 0.002;

    BittrexData(String title) {
        super(title, BTC_USD, LTC_USD, BTC_EUR, LTC_EUR, FEE);
    }

    @Override
    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();
            JsonArray JBids = jsonObject.getJsonObject("result").getJsonArray("buy");
            bids = convertToList(JBids);

            JsonArray JAsks = jsonObject.getJsonObject("result").getJsonArray("sell");
            asks = convertToList(JAsks);

        }
    }

    @Override
    protected ArrayList<double[]> convertToList(JsonArray jarr) {
        ArrayList<double[]> arrayList = new ArrayList<>();
        for (int i = 0; i < jarr.size(); i++) {
            arrayList.add(new double[]{
                    Double.parseDouble(jarr.getJsonObject(i).get("Rate").toString()),
                    Double.parseDouble(jarr.getJsonObject(i).get("Quantity").toString())}
                    );
        }
        return arrayList;
    }
}
