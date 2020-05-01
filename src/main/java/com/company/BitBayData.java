package com.company;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import javax.json.*;


public class BitBayData extends BitData{

    BitBayData(String title) {
        super(title);
    }

    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();

            System.out.println(jsonObject);

            JsonArray JBids = jsonObject.getJsonArray("bids");
            bidsUSD = convertToList(JBids);
            JsonArray JAsks = jsonObject.getJsonArray("asks");
            asksUSD = convertToList(JAsks);

        }
    }

    protected ArrayList<Double> convertToList(JsonArray jarr) {
        ArrayList<Double> arrayList = new ArrayList<>();
        for (int i = 0; i < jarr.size(); i++) {
            arrayList.add(Double.parseDouble(jarr.getJsonArray(i).get(0).toString()));
        }
        return arrayList;
    }
}