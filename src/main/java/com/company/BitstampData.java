package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

public class BitstampData extends BitData {
    BitstampData(String title) {
        super(title);
    }

    @Override
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

    @Override
    protected ArrayList<Double> convertToList(JsonArray jarr) {
        ArrayList<Double> arrayList = new ArrayList<>();
        String numInString;
        for (int i = 0; i < jarr.size(); i++) {
            numInString = jarr.getJsonArray(i).get(0).toString();
            arrayList.add(Double.parseDouble(numInString.substring(1,numInString.length()-1)));
        }
        return arrayList;
    }
}
