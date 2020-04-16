package com.company;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.http.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.concurrent.TimeUnit;
import javax.json.*;


public class BitBayData {

    private ArrayList<Double> asks = new ArrayList<>();
    private ArrayList<Double> bids = new ArrayList<>();
    private LocalDateTime timeOfLastFetch;

    public void getData() throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://bitbay.net/API/Public/BTC/orderbook.json"))
                .build();

        HttpResponse<InputStream> response =
                client.send(request, HttpResponse.BodyHandlers.ofInputStream());

        timeOfLastFetch = LocalDateTime.now();
        int responseCode = response.statusCode();

        if (responseCode == 200) {
            readData(response.body());
        }
        else {
            System.out.println("No connection. Status code: " + responseCode);
        }

        response.body().close();
    }

    public void readData(InputStream input) throws IOException {
        JsonReaderFactory readerFactory = Json.createReaderFactory(Collections.emptyMap());

        try (JsonReader jsonReader = readerFactory.createReader(input)) {
            JsonObject jsonObject = jsonReader.readObject();

            JsonArray JBids = jsonObject.getJsonArray("bids");
            bids = convertJarrayToList(JBids);
            JsonArray JAsks = jsonObject.getJsonArray("asks");
            asks = convertJarrayToList(JAsks);

        }
    }

    private ArrayList<Double> convertJarrayToList(JsonArray jarr) {
        ArrayList<Double> arrayList = new ArrayList<>();
        for (int i = 0; i < jarr.size(); i++) {
            arrayList.add(Double.parseDouble(jarr.getJsonArray(i).get(0).toString()));
        }
        return arrayList;
    }

    public void printBids(int amount) {
        if(bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Bids from BitBay, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(bids.size(),amount); i++) {
            System.out.println(bids.get(i));
        }
    }

    public void printAsks(int amount) {
        if(bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Asks from BitBay, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(asks.size(),amount); i++) {
            System.out.println(asks.get(i));
        }
    }

    public void printDiff(int amount) {
        if(asks.size() == 0 || bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Analysis BitBay, time " + timeOfLastFetch + ": ");
        System.out.println("Bid:    Ask:   ");
        for (int i = 0; i < Math.min(asks.size(), amount); i++) {
            System.out.printf("%.2f %.2f %.2f%s \n", bids.get(i), asks.get(i), getDiff(bids.get(i), asks.get(i)), '%');
        }
    }

    private double getDiff(double bid, double ask) {
        return (1 - (ask - bid))/bid;
    }

    public void analysisDate(int amountOfDate) throws InterruptedException, IOException {
        while(true) {
            getData();
            printDiff(amountOfDate);
            TimeUnit.SECONDS.sleep(5);
        }

    }
}