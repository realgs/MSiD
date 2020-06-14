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
            int lowest_i = 0;
            int highest_i = 0;
            float highest_bid_temp = list.get(0).getBid_prize();
            float lowest_ask_temp = list.get(0).getAsk_prize();
            for (int i = 0; i < list.size(); i++) {
                if (list.get(i).getCurrency() == list.get(highest_i).getCurrency()) {
                    if (highest_bid_temp < list.get(i).getBid_prize()) {
                        highest_bid_temp = list.get(i).getBid_prize();
                        highest_i = i;
                    }
                    if (lowest_ask_temp > list.get(i).getAsk_prize()) {
                        lowest_ask_temp = list.get(i).getAsk_prize();
                        lowest_i = i;
                    }
                }
            }
            Observer high = list.get(highest_i);
            Observer low = list.get(lowest_i);
                float amount = Math.min(list.get(highest_i).getBid_quant(), list.get(lowest_i).getAsk_quant());
                float profit = amount * ((1 - list.get(highest_i).getFee()) * list.get(highest_i).getBid_prize() - (1 - list.get(lowest_i).getFee()) * list.get(lowest_i).getAsk_prize());
                wallet += profit;
                System.out.println("On stock "+low.getName()+ " we can buy " + amount + " " +low.getCurrency()+ " for " +
                        low.getAsk_prize() + " USD and sell on stock " + high.getName() + " for "  +high.getBid_prize() +
                        " and make "+ profit + " $ profit.");
    }
    private static void refresh() {
        while (true) {
            try {
                try {
                    ArrayList<Observer> list = new ArrayList<>();
                list.add(Observer.getDataBitbay("BTC", "USD", "BTC"));
                list.add(Observer.getDataBittrex("USD", "BTC","BTC"));
                list.add(Observer.getDataBitstamp("btc", "usd","BTC"));
                list.add(Observer.getDataBitfinex("BTC", "USD","BTC"));
                list.add(Observer.getDataBitbay("LTC", "USD","LTC"));
                list.add(Observer.getDataBittrex("USD", "LTC","LTC"));
                list.add(Observer.getDataBitstamp("ltc", "usd","LTC"));
                list.add(Observer.getDataBitfinex("LTC", "USD","LTC"));
                Main.makeTransaction(list);
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (ParseException e) {
                    e.printStackTrace();
                }
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}