package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

public class CexData extends BitData{

    public static final String BTC_USD = "https://cex.io/api/order_book/BTC/USD/";
    public static final String LTC_USD = "https://cex.io/api/order_book/LTC/USD/";
    public static final String BTC_EUR = "https://cex.io/api/order_book/BTC/EUR/";
    public static final String BTC_ETH = "https://cex.io/api/order_book/LTC/EUR/";
    public static final double FEE = 0.0025;

    CexData(String title) {
        super(title,BTC_USD, LTC_USD, BTC_EUR, BTC_ETH, FEE);
    }

    @Override
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
