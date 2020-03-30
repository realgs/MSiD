import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class BitBayContent {

    private static String getJString(URL url) throws IOException {
        URLConnection connection = url.openConnection();
        connection.connect();
        BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String content;
        while ((content = br.readLine()) != null) {
            sb.append(content).append("\n");
        }
        br.close();
        return sb.toString();
    }

    private static void printData(String json) throws ParseException {
        if (json != null) {
            JSONParser parser = new JSONParser();
            JSONObject jsonObject = (JSONObject) parser.parse(json);
            JSONArray bids = (JSONArray) jsonObject.get("bids");
            JSONArray asks = (JSONArray) jsonObject.get("asks");

            for (int i = 0; i < bids.size(); i++) {
                System.out.print("Bids - " + bids.get(i) + " | Asks - " + asks.get(i));
                System.out.println();
            }
        }
    }


    public static void main(String[] args) throws Exception {
        URL bitBayUrl = new URL("https://bitbay.net/API/Public/BTC/orderbook.json");
        printData(getJString(bitBayUrl));

    }
}
