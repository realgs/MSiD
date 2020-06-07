import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Iterator;

public class Observer {

    static void getData(String currency1, String currency2) throws IOException, ParseException {
        URL url = new URL("https://bitbay.net/API/Public/"+ currency1  + currency2 +"/orderbook.json");
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject data = (JSONObject) obj;

        if (data != null) {
            JSONArray bids = (JSONArray) data.get("bids");
            JSONArray asks = (JSONArray) data.get("asks");

            Iterator itr1 = bids.iterator();
            Iterator itr2 = asks.iterator();
            while (itr2.hasNext()) {
               {
                    ArrayList bid = (ArrayList) itr1.next();
                    ArrayList ask = (ArrayList) itr2.next();

                    float bid_price = Float.valueOf(bid.get(0).toString());
                    float ask_price = Float.valueOf(ask.get(0).toString());

                    float dif = 1 - ((ask_price - bid_price) / bid_price);
                    System.out.println("Bid= " + bid_price + "\t Ask = " + ask_price + "\t Difference = " + dif+ "%");

                }
            }
        }
        b_reader.close();
    }
}
