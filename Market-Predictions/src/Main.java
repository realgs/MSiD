import org.json.simple.parser.ParseException;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    private static float wallet;
    public static void main(String[] args) {
        try {
            Thread thread = new Thread(Main::refresh);
            thread.setDaemon(true);
            thread.start();
            thread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    public static void makeTransaction(ArrayList<Observer> list) {

        for (int i = 0; i < list.size(); i++) {
            int lowest_i = i;
            int highest_i = i;
            Observer temp = list.get(i);
            float highest_bid_temp = temp.getBid_prize();
            float lowest_ask_temp = temp.getAsk_prize();
            for (int j = 0; j < list.size(); j++) {
                Observer temp2 = list.get(j);
                if (highest_bid_temp < temp2.getBid_prize()) {
                    highest_bid_temp = temp2.getBid_prize();
                    highest_i = j;
                }
                if (lowest_ask_temp > temp2.getAsk_prize()) {
                    lowest_ask_temp = temp2.getAsk_prize();
                    lowest_i = j;
                }
            }
            float amount = Math.min(list.get(highest_i).getBid_quant(), list.get(lowest_i).getAsk_quant());
            float profit = amount * (1 - list.get(highest_i).getFee()) * list.get(highest_i).getBid_prize() * list.get(lowest_i).getFee()
                    - amount * list.get(lowest_i).getAsk_prize();
            System.out.println(profit);
            if (profit > 0) {
                wallet += profit;
            }
        }
    }

    private static void refresh() {
        while (true) {
            try {
                try {
                   // ArrayList<Observer> list = new ArrayList<Observer>();
                   // list.add(Observer.getDataBitbay("BTC", "USD"));
                   // list.add(Observer.getDataBittrex("USD", "BTC"));
                   // list.add(Observer.getDataBitstamp("btc", "usd"));
                   // list.add(Observer.getDataBitfinex("BTC", "USD"));
                   // Main.makeTransaction(list);
                   // ArrayList<History> list = History.makelist("04-05-2020","10-05-2020");
                   // History.averages(list);
                    //History.medianes(list);
                   // History.averages(History.differences(list));
                    History.predict100("01-06-2020","13-06-2020","10-07-2020");
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (ParseException e) {
                    e.printStackTrace();
                } catch (java.text.ParseException e) {
                    e.printStackTrace();
                }
                Thread.sleep(50000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }
}



