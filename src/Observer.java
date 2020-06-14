import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

public class Observer {
    public float getBid_prize() {
        return bid_prize;
    }
    public float getAsk_prize() {
        return ask_prize;
    }
    public float getBid_quant() {
        return bid_quant;
    }
    public float getAsk_quant() {
        return ask_quant;
    }
    float bid_prize, ask_prize, bid_quant, ask_quant;
    public String getName() {
        return name;
    }
    public float getFee() {
        return fee;
    }
    float fee;
    String name;

    public String getCurrency() {
        return currency;
    }

    String currency;
    public Observer(float bidp, float askp, float bidq, float askq, String sname, String currencyname, float takerFee){
        bid_prize =bidp;
        ask_prize = askp;
        bid_quant = bidq;
        ask_quant = askq;
        name = sname;
        currency = currencyname;
        fee = takerFee;
    }

    static Observer getDataBitbay(String currency1, String currency2, String currencyName) throws IOException, ParseException {
        URL url = new URL("https://bitbay.net/API/Public/"+ currency1  + currency2 +"/orderbook.json");
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject data = (JSONObject) obj;
            JSONArray bids = (JSONArray) data.get("bids");
            JSONArray asks = (JSONArray) data.get("asks");
            ArrayList bid = (ArrayList) bids.get(0);
            ArrayList ask = (ArrayList) asks.get(0);
            float bid_price = Float.valueOf(bid.get(0).toString());
            float bid_quant = Float.valueOf(bid.get(1).toString());
            float ask_price = Float.valueOf(ask.get(0).toString());
            float ask_quant = Float.valueOf(ask.get(1).toString());
            System.out.println("Bid= " + bid_price + "\t Quantity= " + bid_quant + "\t Ask = " + ask_price + "\t Quantitiy = " + ask_quant);
         Observer ob1 = new Observer(bid_price, ask_price, bid_quant, ask_quant, "Bitbay", currencyName, (float) 0.0001);
        b_reader.close();
        return ob1;
    }
    static Observer getDataBittrex(String currency1, String currency2, String currencyName) throws IOException, ParseException {
        URL url = new URL("https://api.bittrex.com/api/v1.1/public/getorderbook?market="+ currency1  +"-"+ currency2 +"&type=both");
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject data = (JSONObject) obj;

            JSONObject results = (JSONObject) data.get("result");
            JSONArray bids = (JSONArray) results.get("buy");
            JSONArray asks = (JSONArray) results.get("sell");
            JSONObject bid = (JSONObject) bids.get(0);
            JSONObject ask = (JSONObject) bids.get(0);
            float bid_price = Float.valueOf(bid.get("Rate").toString());
            float bid_quant = Float.valueOf(bid.get("Quantity").toString());
            float ask_price = Float.valueOf(ask.get("Rate").toString());
            float ask_quant = Float.valueOf(ask.get("Quantity").toString());
            System.out.println("Bid= " + bid_price + "\t Quantity= " + bid_quant + "\t Ask = " + ask_price + "\t Quantitiy = " + ask_quant);
            Observer ob1 = new Observer(bid_price, ask_price, bid_quant, ask_quant, "Bittrex", currencyName, (float)0.0002);
        b_reader.close();
        return ob1;
    }
    static Observer getDataBitstamp(String currency1, String currency2, String currencyName) throws IOException, ParseException {
        URL url = new URL("https://www.bitstamp.net/api/v2/order_book/"+ currency1  + currency2 +"/");
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject data = (JSONObject) obj;
            JSONArray bids = (JSONArray) data.get("bids");
            JSONArray asks = (JSONArray) data.get("asks");
            ArrayList bid = (ArrayList) bids.get(0);
            ArrayList ask = (ArrayList) asks.get(0);
            float bid_price = Float.valueOf(bid.get(0).toString());
            float bid_quant = Float.valueOf(bid.get(1).toString());
            float ask_price = Float.valueOf(ask.get(0).toString());
            float ask_quant = Float.valueOf(ask.get(1).toString());
            System.out.println("Bid= " + bid_price + "\t Quantity= " + bid_quant + "\t Ask = " + ask_price + "\t Quantitiy = " + ask_quant);
        Observer ob1 = new Observer(bid_price, ask_price, bid_quant, ask_quant, "Bittstamp", currencyName, (float)0.00025);
        b_reader.close();
        return ob1;
    }

    static Observer getDataBitfinex(String currency1, String currency2, String currencyName) throws IOException, ParseException {
        URL url = new URL("https://api.bitfinex.com/v1/book/" + currency1 + currency2);
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject data = (JSONObject) obj;

        JSONArray bids = (JSONArray) data.get("bids");
        JSONArray asks = (JSONArray) data.get("asks");
        JSONObject bid = (JSONObject) bids.get(0);
        JSONObject ask = (JSONObject) bids.get(0);
        float bid_price = Float.valueOf(bid.get("price").toString());
        float bid_quant = Float.valueOf(bid.get("amount").toString());
        float ask_price = Float.valueOf(ask.get("price").toString());
        float ask_quant = Float.valueOf(ask.get("amount").toString());
        System.out.println("Bid= " + bid_price + "\t Quantity= " + bid_quant + "\t Ask = " + ask_price + "\t Quantitiy = " + ask_quant);

        Observer ob1 = new Observer(bid_price, ask_price, bid_quant, ask_quant, "Bitfinex", currencyName,(float)0.0002);
        b_reader.close();
        return ob1;
    }

}
