package base;

import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Date;

public class history_provider
{
    private String currency_url;

    public history_provider(String currency)
    {
        currency_url = "https://api.coingecko.com/api/v3/coins/" +  currency + "/history?localization=false&date=";
    }

    public data obtain_data(String date) // 23-03-2015
    {
        data historical_data = new data();
        try
        {
            URLConnection conn = new URL(currency_url + date).openConnection();
            try
            {
                BufferedReader buffered_reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                try
                {
                    String line;
                    if ((line = buffered_reader.readLine()) != null)
                    {
                        historical_data = get_data_from_json_string(line);
//                        System.out.println(data);
                    }
                }
                catch (EOFException ignored) { }

                buffered_reader.close();
            }
            catch (IOException e) { e.printStackTrace(); }
        }
        catch (MalformedURLException e)
        {
            System.out.println("Invalid URL for " + currency_url);
            e.printStackTrace();
        }
        catch (IOException e) { e.printStackTrace(); }

        return historical_data;
    }

    private data get_data_from_json_string(String json_string)
    {
//        System.out.println(json_string);
//        return new data();

        if(json_string == null) return new data();

        float price = 0f, volume = 0f;
        try
        {
            int current_price_start_position = json_string.indexOf( "\"current_price\":{" );
            int price_start_position = json_string.indexOf("\"usd\":", current_price_start_position ) + 6;
            int price_end_position = json_string.indexOf(',', price_start_position );

            int current_volume_start_position = json_string.indexOf( "\"total_volume\":{" );
            int volume_start_position = json_string.indexOf("\"usd\":", current_volume_start_position ) + 6;
            int volume_end_position = json_string.indexOf(',', volume_start_position );

            price = Float.parseFloat( json_string.substring(price_start_position, price_end_position ) );
            volume = Float.parseFloat( json_string.substring(volume_start_position, volume_end_position ) );
        }
        catch (java.lang.NumberFormatException ignored){ /* System.out.println(ignored); */ }

        return new data(price, volume);
    }

    public ArrayList<data> provide_data(String date_from, String date_to) // 23-03-2015
    {
        ArrayList<data> historical_data = new ArrayList<data>();

        try
        {
            SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy"); // 23-03-2015
            SimpleDateFormat reversed_formatter = new SimpleDateFormat("yyyy-MM-dd"); // 2015-03-23
            Date startDate = formatter.parse(date_from);
            Date endDate = formatter.parse(date_to);
            LocalDate start = startDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
            LocalDate end = endDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

            for (LocalDate date = start; !date.isAfter(end); date = date.plusDays(1))
            {
//                System.out.println(formatter.format(reversed_formatter.parse(date.toString())));
                historical_data.add(obtain_data(formatter.format(reversed_formatter.parse(date.toString()))));
            }

        }
        catch (ParseException e) { e.printStackTrace(); }

        return historical_data;
    }
}
