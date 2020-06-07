package market_observer;

import java.io.*;
import java.net.*;

public class bitbay_observer extends market_observer
{
    private URL currency_url;

    public bitbay_observer(String currency)
    {
        super(currency, "bitbay");
        try
        {
            currency_url = new URL("https://bitbay.net/API/Public/"+  currency + "/ticker.json");
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
        if(json_string == null) return;

        try
        {
            float bid = Float.parseFloat( json_string.substring( json_string.indexOf("\"bid\":") + 6,
                    json_string.indexOf(',', json_string.indexOf( "\"bid\":" ) ) ) );
            float ask = Float.parseFloat( json_string.substring( json_string.indexOf("\"ask\":") + 6,
                    json_string.indexOf(',', json_string.indexOf( "\"ask\":") ) ) );

            bid_price = bid;
            ask_price = ask;

//            System.out.println("bid: "+ bid + ", ask: " + ask);
        }
        catch (java.lang.NumberFormatException ignored){}

    }
}
