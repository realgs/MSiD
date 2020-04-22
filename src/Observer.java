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

//Returns an object which consists of 2 keys: bids and asks, which are sequentially arrays of purchase and sell orders.
//Units of this arrays are also arrays and consist of 2 elements. The first one is rate, and second is an amount of cryptocurrency in that order.
//bids is buying, asks is selling
public class Observer {

    static void getData() throws IOException, ParseException {
        URL url = new URL("https://bitbay.net/API/Public/BTC/orderbook.json");
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

                    System.out.println("Bid= " + bid.get(0) + "\t Ask = " + ask.get(0));

                }
            }


        }
        b_reader.close();
    }


}
