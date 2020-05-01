package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

public class BittrexData extends BitData{

    BittrexData(String title) {
        super(title);
    }

    @Override
    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();

            JsonArray JBids = jsonObject.getJsonObject("result").getJsonArray("buy");
            bidsUSD = convertToList(JBids);

            JsonArray JAsks = jsonObject.getJsonObject("result").getJsonArray("sell");
            asksUSD = convertToList(JAsks);

        }
    }

    protected ArrayList<Double> convertToList(JsonArray jarr) {
        ArrayList<Double> arrayList = new ArrayList<>();
        for (int i = 0; i < jarr.size(); i++) {
            arrayList.add(Double.parseDouble(jarr.getJsonObject(i).get("Rate").toString()));
        }
        return arrayList;
    }
}
