import kong.unirest.Unirest;
import kong.unirest.json.JSONArray;
import javafx.util.Pair;
import java.util.List;
import java.util.concurrent.TimeUnit;


public class App {
    public static void main(String[] args) {

        try {
            printEvery5Seconds("BTC", "PLN",10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    static void printEvery5Seconds(String currency1, String currency2, int offersAmount) throws InterruptedException{
        while (true) {
            var offers = getOffers(currency1, currency2);
            printOffers(offers.getKey().toList(), offers.getValue().toList(), offersAmount);
            double bestBuy = ((JSONArray)offers.getValue().get(0)).getDouble(0);
            double bestSell = ((JSONArray)offers.getKey().get(0)).getDouble(0);
            double difference = getDiff(bestBuy, bestSell);
            System.out.print("Difference: "  + difference + "%");
            TimeUnit.SECONDS.sleep(5);
        }
    }

    static double getDiff(double buy, double sell) {
        return Math.round((1.d - (sell - buy) / buy) * 1000.d) / 1000.d;

    }

    static void printOffers(List sellOffers, List buyOffers, int offersAmount) {
        System.out.println("sale offers(rate,amount):");
        printList(sellOffers, offersAmount);
        System.out.println("purchase offers(rate,amount):");
        printList(buyOffers, offersAmount);
    }

    static <T> void printList(List<T> list, int size) {
        size = Math.min(size, list.size());
        for (int i = 0; i < size; i++) {
            System.out.println(list.get(i));
        }
    }

    static Pair<JSONArray, JSONArray> getOffers(String currency1, String currency2) {
        String url = "https://bitbay.net/API/Public/" + currency1 + currency2 + "/orderbook.json";
        var response = Unirest.get(url).asJson().getBody().getObject();
        var sell = response.getJSONArray("asks");
        var buy = response.getJSONArray("bids");
        return new Pair<>(sell,buy);
    }

    static void printOnce(String currency1, String currency2, int offersAmount) {
        var offers = getOffers(currency1, currency2);
        var sell = offers.getKey().toList();
        var buy = offers.getValue().toList();
        printOffers(sell,buy,offersAmount);
    }
}
