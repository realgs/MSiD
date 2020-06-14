import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.Random;

public class History {
    float price;
    public float getPrice() {
        return price;
    }
    public float getMarket_cap() {
        return market_cap;
    }
    public float getVolume() {
        return volume;
    }
    public String getDate() {
        return date;
    }
    float market_cap;
    float volume;
    String date;
    public  History(float p, float mc, float v, String d){
        price =p;
        market_cap = mc;
        volume = v;
        date =d;
    }
    static History getData(String date1) throws IOException, ParseException {
        URL url = new URL("https://api.coingecko.com/api/v3/coins/bitcoin/history?date="+ date1 +"&localization=false");
        URLConnection connection = url.openConnection();
        BufferedReader b_reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        Object obj = new JSONParser().parse(new BufferedReader(new InputStreamReader(connection.getInputStream())));
        JSONObject mdata = (JSONObject) obj;
        JSONObject data = (JSONObject) mdata.get("market_data");
        JSONObject prices = (JSONObject) data.get("current_price");
        float price = Float.valueOf(prices.get("usd").toString());
        JSONObject caps = (JSONObject) data.get("market_cap");
        float cap = Float.valueOf(caps.get("usd").toString());
        JSONObject volumes = (JSONObject) data.get("total_volume");
        float volume =  Float.valueOf(volumes.get("usd").toString());
        History ob1 = new History(price, cap, volume, date1);
        b_reader.close();
        return ob1;
    }

    public static ArrayList<History> makelist(String sDate, String eDate) throws IOException, ParseException, java.text.ParseException {
        ArrayList<History> list = new ArrayList<History>();
        SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy");
        Date date       = format.parse ( sDate );
        Date dateEnd = format.parse(eDate);
        LocalDate start = date.toInstant().atZone(ZoneOffset.UTC).toLocalDate();
        LocalDate end = dateEnd.toInstant().atZone(ZoneOffset.UTC).toLocalDate();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");

        for (LocalDate i=start; i.isBefore(end); i = i.plusDays(1)){
            History h = getData(format.format(formatter.parse(i.toString())));
            list.add(h);
        }
        return list;
    }
    public static ArrayList<History> differences(ArrayList<History> list){
        float price_diff;
        float cap_diff;
        float volume_diff;
        ArrayList<History> diff_list = new ArrayList<History>();
        for(int i=0; i<(list.size()-1);i++){
            price_diff = (list.get(i+1).getPrice() -list.get(i).getPrice())/list.get(i).getPrice();
            cap_diff=   (list.get(i+1).getMarket_cap() -list.get(i).getMarket_cap())/list.get(i).getMarket_cap();
            volume_diff = (list.get(i+1).getVolume() -list.get(i).getVolume())/list.get(i).getVolume();
            History diff = new History(price_diff,cap_diff,volume_diff,"");
            diff_list.add(diff);
        }
        return diff_list;
    }
    public static History averages(ArrayList<History> list){
        float price_average = 0;
        float cap_average =0;
        float volume_average=0;
        for (int i=0; i<list.size(); i++){
            price_average+= list.get(i).getPrice();
            cap_average+= list.get(i).getMarket_cap();
            volume_average+= list.get(i).getVolume();
        }
        History ob = new History(price_average/list.size(),cap_average/list.size(),volume_average/list.size(),"");
        //System.out.println("Averges: Price = "+ price_average/list.size() + "\t Cap = " + cap_average/list.size() + "\t Volume=" + volume_average/list.size());
        return ob;
    }
    public static History medianes(ArrayList<History> list){
        ArrayList<Float> prices = new ArrayList<Float>();
        ArrayList<Float> caps = new ArrayList<Float>();
        ArrayList<Float> volumes = new ArrayList<Float>();
        float temp_price;
        float temp_cap;
        float temp_volume;
        for(int i=0;i<list.size();i++){
           temp_price = list.get(i).getPrice();
           prices.add(temp_price);
            temp_cap = list.get(i).getMarket_cap();
            caps.add(temp_cap);
            temp_volume = list.get(i).getVolume();
            volumes.add(temp_volume);
        }
        prices.sort(Comparator.naturalOrder());
        caps.sort(Comparator.naturalOrder());
        volumes.sort(Comparator.naturalOrder());
        int middle_index = ((list.size()/2)-1);
        History medians = new History(prices.get(middle_index), caps.get(middle_index),volumes.get(middle_index),"");
        //System.out.println("Medians: price = " + medians.getPrice() + "\t Capacity = "+medians.getMarket_cap()+ "\t Volume= "+medians.getVolume());
        return medians;

    }
    public static History upOrDown(ArrayList<History>list){
        float price_ups =0;
        float cap_ups = 0;
        float vol_ups =0;
        for( int i=0; i<(list.size()-1);i++){
            if(list.get(i).getPrice()<list.get(i+1).getPrice())
                price_ups++;
            if(list.get(i).getMarket_cap()<list.get(i+1).getMarket_cap())
                cap_ups++;
            if(list.get(i).getVolume()<list.get(i+1).getVolume())
                vol_ups++;
        }
        price_ups = price_ups/list.size();
        cap_ups = cap_ups/list.size();
        vol_ups = vol_ups/list.size();
        History ups = new History(price_ups,cap_ups,vol_ups,"");
        return ups;
    }

    public static ArrayList<History> predict(String date_from, String date_to, String future_date) throws ParseException, java.text.ParseException, IOException {
        ArrayList<History> historical_data = History.makelist(date_from,date_to);
        ArrayList<History> future_data = new ArrayList<History>();

        SimpleDateFormat format = new SimpleDateFormat("dd-MM-yyyy");
        Date date       = format.parse ( date_to );
        Date dateF      = format.parse ( future_date );
        LocalDate future = date.toInstant().atZone(ZoneOffset.UTC).toLocalDate();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        int duration = (int) ChronoUnit.DAYS.between(date.toInstant(), dateF.toInstant());
        float price_up = upOrDown(historical_data).getPrice();
        float cap_up = upOrDown(historical_data).getMarket_cap();
        float vol_up = upOrDown(historical_data).getVolume();
        float average_diff_price = (History.averages(History.differences(historical_data))).getPrice();
        float average_diff_cap = (History.averages(History.differences(historical_data))).getMarket_cap();
        float average_diff_vol = (History.averages(History.differences(historical_data))).getVolume();
        float temp_price = historical_data.get(historical_data.size()-1).getPrice();
        float temp_cap = historical_data.get(historical_data.size()-1).getMarket_cap();
        float temp_vol = historical_data.get(historical_data.size()-1).getVolume();
        for (int i = 0; i<duration; i++){
            Random random = new Random();
            float r = (random.nextFloat()*2);
            if(price_up*r<0.5)
            temp_price -= temp_price*(10*average_diff_price);
            else
                temp_price+=temp_price*(10*average_diff_price);
            if(cap_up*r<0.5)
                temp_cap -=temp_cap*(10*average_diff_cap);
            else
                temp_cap+=temp_cap*(10*average_diff_cap);
            if(vol_up*r<0.5)
                temp_vol-=temp_vol*(10*average_diff_vol);
            else
                temp_vol+=temp_vol*(10*average_diff_vol);

            future = future.plusDays(1);
            String temp_date = format.format(formatter.parse(future.toString()));
            future_data.add(new History(temp_price, temp_cap, temp_vol, temp_date));
           // System.out.println("Predict: Price = "+ temp_price + "\t Cap = " + temp_cap + "\t Volume=" + temp_vol +"\t Data = " +temp_date);

        }
        return future_data;

    }
    public static ArrayList<History> predict100(String date_from, String date_to, String future_date) throws ParseException, java.text.ParseException, IOException {
        ArrayList<ArrayList<History>> preditions = new ArrayList<>();
        ArrayList<History> average_pred = new ArrayList<>();
        for(int i=0; i<100;i++){
            preditions.add(predict(date_from, date_to, future_date));
        }
        for(int k=0;k<preditions.get(0).size();k++){
            float price_average = 0;
            float cap_average =0;
            float volume_average=0;
            String date = "";
            for (int j=0; j<preditions.size(); j++){
                price_average+= preditions.get(j).get(k).getPrice();
                cap_average+= preditions.get(j).get(k).getMarket_cap();
                volume_average+= preditions.get(j).get(k).getVolume();
                date = preditions.get(j).get(k).getDate();
            }
            History ob = new History(price_average/preditions.size(),cap_average/preditions.size(),volume_average/preditions.size(), date);
            average_pred.add(ob);
            System.out.println("Averges: Price = "+ price_average/preditions.size() + "\t Cap = " + cap_average/preditions.size() + "\t Volume=" + volume_average/preditions.size() + "\t Date = " + date);
        }
        return average_pred;

    }

};
