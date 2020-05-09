package market_observer;

import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class bybit_observer extends market_observer
{
    private URL currency_url;

    public bybit_observer(String currency)
    {
        super(currency, "bybit", 0.0007f);
        try
        {
            currency_url = new URL("https://api.bybit.com/v2/public/orderBook/L2?symbol="+  currency + "USD");
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
            int bid_price_start_position = json_string.indexOf("\"price\":\"") + 9;
            int bid_price_end_position = json_string.indexOf("\",\"size\":", bid_price_start_position );
            int bid_amount_end_position = json_string.indexOf(',', bid_price_end_position + 9);

            int first_sell_position = json_string.indexOf("Sell") - 40;

            int ask_price_start_position = json_string.indexOf("\"price\":\"", first_sell_position ) + 9;
            int ask_price_end_position = json_string.indexOf("\",\"size\":", ask_price_start_position );
            int ask_amount_end_position = json_string.indexOf(',', ask_price_end_position + 9);

            bid_price = Float.parseFloat( json_string.substring(bid_price_start_position, bid_price_end_position ) );
            bid_amount = Float.parseFloat( json_string.substring(bid_price_end_position + 9, bid_amount_end_position ) ) / bid_price;

            ask_price = Float.parseFloat( json_string.substring(ask_price_start_position, ask_price_end_position ) );
            ask_amount = Float.parseFloat( json_string.substring(ask_price_end_position + 9, ask_amount_end_position ) ) / ask_price;

//            System.out.println("bid: " + bid_amount + " ✖️ " + bid_price + "; ask: " + ask_amount + " ✖️ " + ask_price);
        }
        catch (NumberFormatException ignored){ /* System.out.println(ignored); */ }

    }
}
