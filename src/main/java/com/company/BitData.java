package com.company;

import javax.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

public abstract class BitData {

    String title = "";
    protected ArrayList<Double> asksUSD = new ArrayList<>();
    protected ArrayList<Double> bidsUSD = new ArrayList<>();
    protected LocalDateTime timeOfLastFetch;

    BitData(String title){
        this.title = title;
    }

    public void getData(String endpoint) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(endpoint))
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

    abstract public void readData(InputStream input) throws IOException;

    abstract protected ArrayList<Double> convertToList(JsonArray jarr);

    public void printBids(int amount) {
        if(bidsUSD.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Bids, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(bidsUSD.size(),amount); i++) {
            System.out.println(bidsUSD.get(i));
        }
    }

    public void printAsks(int amount) {
        if(bidsUSD.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Asks, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(asksUSD.size(),amount); i++) {
            System.out.println(asksUSD.get(i));
        }
    }

    public void printDiff(int amount) {
        if(asksUSD.size() == 0 || bidsUSD.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Analysis, time " + timeOfLastFetch + ": ");
        System.out.println("Bid:    Ask:   ");
        for (int i = 0; i < Math.min(asksUSD.size(), amount); i++) {
            System.out.printf("%.2f %.2f %.2f%s \n", bidsUSD.get(i), asksUSD.get(i), getDiff(bidsUSD.get(i), asksUSD.get(i)), '%');
        }
    }

    protected double getDiff(double bid, double ask) {
        return (1 - (ask - bid))/bid;
    }

    public void analysisDate(int amountOfDate, String endpoint) throws InterruptedException, IOException {
        while(true) {
            getData(endpoint);
            printDiff(amountOfDate);
            TimeUnit.SECONDS.sleep(5);
        }

    }
}
