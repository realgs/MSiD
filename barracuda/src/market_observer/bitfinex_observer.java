package market_observer;

import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class bitfinex_observer extends market_observer
{
    private URL currency_url;

    public bitfinex_observer(String currency)
    {
        super(currency, "bitfinex", 0.002f);
        try
        {
            currency_url = new URL("https://api-pub.bitfinex.com/v2/ticker/t"+  currency + "USD");
            update_data();
            print_status();
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
            int bid_price_start_position = json_string.indexOf('[') + 1;
            int bid_amount_start_position = json_string.indexOf(',', bid_price_start_position ) + 1;
            int ask_price_start_position = json_string.indexOf(',', bid_amount_start_position) + 1;
            int ask_amount_start_position = json_string.indexOf(',', ask_price_start_position ) + 1;
            int ask_amount_end_position = json_string.indexOf(',', ask_amount_start_position ) - 1;
//
            bid_price = Float.parseFloat( json_string.substring(bid_price_start_position, bid_amount_start_position - 1 ) );
            bid_amount = Float.parseFloat( json_string.substring(bid_amount_start_position, ask_price_start_position - 2 ) );

            ask_price = Float.parseFloat( json_string.substring(ask_price_start_position, ask_amount_start_position - 1 ) );
            ask_amount = Float.parseFloat( json_string.substring(ask_amount_start_position, ask_amount_end_position ) );
//
////            System.out.println("bid: " + bid_amount + " ✖️ " + bid_price + "; ask: " + ask_amount + " ✖️ " + ask_price);
        }
        catch (NumberFormatException ignored){ /* System.out.println(ignored); */ }

    }
}
