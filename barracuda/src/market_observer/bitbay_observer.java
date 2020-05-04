package market_observer;

import java.io.*;
import java.net.*;

public class bitbay_observer extends market_observer
{
    private URL currency_url;

    public bitbay_observer(String currency)
    {
        super(currency, "bitbay", 0.005f);
        try
        {
            currency_url = new URL("https://bitbay.net/API/Public/"+  currency + "/orderbook.json");
            update_data();
        }
        catch (MalformedURLException e)
        {
            System.out.println("Invalid URL for " + currency);
            e.printStackTrace();
        }
    }

    @Override
    public void update_data()
    {
        try
        {
            URLConnection conn = currency_url.openConnection();
            try
            {
                BufferedReader buffered_reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                try
                {
                    String line;
                    if ((line = buffered_reader.readLine()) != null) get_data_from_json_string(line);
                }
                catch (EOFException ignored) { }

                buffered_reader.close();
            }
            catch (IOException e) { e.printStackTrace(); }
        }
        catch (IOException e) { e.printStackTrace(); }
    }

    private void get_data_from_json_string(String json_string)
    {
//        System.out.println(json_string);
//        return;
        if(json_string == null) return;

        try
        {
            int bid_price_start_position = json_string.indexOf("\"bids\":[[") + 9;
            int bid_price_end_position = json_string.indexOf(',', bid_price_start_position );
            int bid_amount_end_position = json_string.indexOf(']', bid_price_end_position );

            int ask_price_start_position = json_string.indexOf("\"asks\":[[") + 9;
            int ask_price_end_position = json_string.indexOf(',', ask_price_start_position );
            int ask_amount_end_position = json_string.indexOf(']', ask_price_end_position );

            bid_price = Float.parseFloat( json_string.substring(bid_price_start_position, bid_price_end_position ) );
            bid_amount = Float.parseFloat( json_string.substring(bid_price_end_position + 1, bid_amount_end_position ) );

            ask_price = Float.parseFloat( json_string.substring(ask_price_start_position, ask_price_end_position ) );
            ask_amount = Float.parseFloat( json_string.substring(ask_price_end_position + 1, ask_amount_end_position ) );

//            System.out.println("bid: " + bid_amount + " ✖️ " + bid_price + "; ask: " + ask_amount + " ✖️ " + ask_price);
        }
        catch (java.lang.NumberFormatException ignored){ /* System.out.println(ignored); */ }

    }
}