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
    protected String endpointBTCUSD, endpointLTCUSD, endpointBTCEUR, endpointLTCEUR;
    protected String title = "";
    protected ArrayList<double[]> asks = new ArrayList<>();
    protected ArrayList<double[]> bids = new ArrayList<>();
    protected LocalDateTime timeOfLastFetch;

    BitData(String title, String endpointBTCUSD, String endpointLTCUSD, String endpointBTCEUR, String endpointLTCEUR){
        this.title = title;
        this.endpointBTCUSD = endpointBTCUSD;
        this.endpointLTCUSD = endpointLTCUSD;
        this.endpointBTCEUR = endpointBTCEUR;
        this.endpointLTCEUR = endpointLTCEUR;
    }

    public boolean getDataBTCUSD() throws IOException, InterruptedException {
        return getData(endpointBTCUSD);
    }

    public boolean getDataLTCUSD() throws IOException, InterruptedException {
        return getData(endpointLTCUSD);
    }

    public boolean getDataBTCEUR() throws IOException, InterruptedException {
        return getData(endpointBTCEUR);
    }

    public boolean getDataLTCEUR() throws IOException, InterruptedException {
        return getData(endpointLTCEUR);
    }

    private boolean getData(String endpoint) throws IOException, InterruptedException {
        if(endpoint=="") return false;
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
            return false;
        }

        response.body().close();
        return true;
    }

    abstract public void readData(InputStream input) throws IOException;

    abstract protected ArrayList<double[]> convertToList(JsonArray jarr);

    public double[] getBestAsk() {
        return asks.get(0);
    }//najlepsza oferta sprzedaży

    public double[] getBestBid() {
        return bids.get(0);
    }//najlepsza oferta kupna

    public void printBids(int amount) {
        if(bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Bids, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(bids.size(),amount); i++) {
            System.out.println(bids.get(i)[0]);
        }
    }

    public void printAsks(int amount) {
        if(bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Asks, time " + timeOfLastFetch + ": ");

        for (int i = 0; i < Math.min(asks.size(),amount); i++) {
            System.out.println(asks.get(i)[0]);
        }
    }

    public void printDiff(int amount) {
        if(asks.size() == 0 || bids.size() == 0) {
            System.out.println("No data.");
            return;
        }
        System.out.println("Analysis, time " + timeOfLastFetch + ": ");
        System.out.println("Bid:    Ask:   ");
        for (int i = 0; i < Math.min(asks.size(), amount); i++) {
            System.out.printf("%.2f %.2f %.2f%s \n", bids.get(i)[0], asks.get(i)[0], getDiff(bids.get(i)[0], asks.get(i)[0]), '%');
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

    protected double convertStringToDouble(String numToConvert) {
        String num = numToConvert;
        if(num.charAt(0)=='"') {
            num = num.substring(1);
        }
        if(num.charAt(num.length()-1)=='"') {
            num = num.substring(0,num.length()-1);
        }

        return Double.parseDouble(num);
    }

    public String getTitle(){
        return title;
    }
}
