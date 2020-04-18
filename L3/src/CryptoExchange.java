import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class CryptoExchange {


    private static void printParsedData(String j) throws ParseException {
        if (j != null) {
            JSONParser p = new JSONParser();
            JSONObject o = (JSONObject) p.parse(j);
            JSONArray bid = (JSONArray) o.get("bids");
            JSONArray ask = (JSONArray) o.get("asks");

            for (int i = 0; i < bid.size(); i++) {
                System.out.print("Bids: " + bid.get(i) + " | Asks: " + ask.get(i));
                System.out.println();
            }
        }
    }



    public static void updateData(URL link) throws Exception {
        JSONParser p = new JSONParser();
        String line;

        do {
            line = getJSONString(link);
            JSONObject o = (JSONObject) p.parse(line);
            JSONArray bid = (JSONArray) o.get("BID");
            JSONArray ask = (JSONArray) o.get("ASK");

            for (int k = 0; k < bid.size(); k++) {
                double valueBid = getValueFromString(bid.get(k).toString());
                double valueAsk = getValueFromString(ask.get(k).toString());

                System.out.println(1.0 - (valueBid - valueAsk) / valueAsk);

            }


        }

        while (line != null);

    }



   public static double getValueFromString(String line_2) {
       String num = line_2.split(",")[0].substring(1);

       return Double.parseDouble(num);


   }


   public static String getJSONString(URL link) throws Exception {
       URLConnection c = link.openConnection();
       c.connect();
       BufferedReader reader = new BufferedReader(new InputStreamReader(c.getInputStream()));
       StringBuilder builder = new StringBuilder();



       String keeper;
       while ((keeper = reader.readLine()) != null) {
           builder.append(keeper).append("\n");
       }


       return builder.toString();


   }






    public static void main(String[] args) throws Exception {
        System.out.println();
        System.out.println("BITBAY.NET EXCHANGE BITCOIN CASH RATES: ");
        System.out.println();
        URL cryptoURL = new URL("https://bitbay.net/API/Public/BCC/orderbook.json");
        printParsedData(getJSONString(cryptoURL));
        System.out.println();
        updateData(cryptoURL);

    }






}
