package main;

import market_observer.*;

import java.time.*;
import java.util.ArrayList;

public class Main
{
    private static ArrayList<market_observer> market_observers = new ArrayList<market_observer>();
    private static int refresh_interval;
    private static float wallet;

    private static void refresh()
    {
        System.out.println("\n----- Status for " + Instant.now() + " -----");
        for ( market_observer observer: market_observers )
        {
            observer.update_data();
            observer.print_status();
        }
    }

    private static void make_transactions()
    {
        while (true) make_best_transaction();
    }

    private static void make_best_transaction()
    {
        float best_amount = 0;
        float best_profit = 0;
        int best_seller_index = 0;
        int best_buyer_index = 0;

        for(int i = 0; i < market_observers.size(); i++)
        {
            market_observer comparing = market_observers.get(i);
            int highest_bid_index = i;
            int lowest_ask_index = i;
            float highest_bid = comparing.bid_price();
            float lowest_ask = comparing.ask_price();

            for(int j = 0; j < market_observers.size(); j++)
            {
                market_observer comparing_2 = market_observers.get(j);
                if(comparing.currency() == comparing_2.currency())
                {
                    if(comparing_2.bid_price() > highest_bid)
                    {
                        highest_bid = comparing_2.bid_price();
                        highest_bid_index = j;
                    }
                    if(comparing_2.ask_price() < lowest_ask)
                    {
                        lowest_ask = comparing_2.ask_price();
                        lowest_ask_index = j;
                    }
                }
            }

            market_observer bidder = market_observers.get(highest_bid_index);
            market_observer asker = market_observers.get(lowest_ask_index);

            float current_amount = Math.min(wallet / asker.ask_price(), Math.min(bidder.bid_amount(), asker.ask_amount()));
            float current_profit = current_amount * (1 - asker.commission_fee()) * bidder.bid_price() * (1 - bidder.commission_fee())
                    - current_amount * asker.ask_price();

            if(current_profit > best_profit)
            {
                best_amount = current_amount;
                best_profit = current_profit;
                best_buyer_index = highest_bid_index;
                best_seller_index = lowest_ask_index;
            }

        }

        market_observer best_seller = market_observers.get(best_seller_index);
        market_observer best_buyer = market_observers.get(best_buyer_index);

        if(best_profit >= 0.00005)
        {
            wallet += best_profit;
            best_seller.apply_buying_transaction(best_amount); // buy from them
            best_buyer.apply_selling_transaction(best_amount); // sell them

            System.out.println(
                    "Buying " + best_amount + " of " + best_seller.currency() +
                    " for " + best_amount * best_seller.ask_price() + " USD on " +
                    best_seller.name() + " and selling with a profit of " + best_profit +
                    " on " + best_buyer.name() + "; current wallet is $" + wallet
                    );
        }
    }

    private static void refresh_periodically()
    {
        while (true)
        {
            refresh();
            try
            {
                Thread.sleep(refresh_interval);
            }
            catch(InterruptedException ex)
            {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args)
    {
        wallet = 100000;
        refresh_interval = 4000;

        market_observers.add(new bitbay_observer("BTC"));
        market_observers.add(new bybit_observer("BTC"));
        market_observers.add(new bitfinex_observer("BTC"));
//        market_observers.add(new whitebit_observer("BTC"));


        market_observers.add(new bitbay_observer("ETH"));
        market_observers.add(new bybit_observer("ETH"));
        market_observers.add(new bitfinex_observer("ETH"));

//        market_observers.add(new bitbay_observer("LSK"));
//        market_observers.add(new bitbay_observer("GAME"));
//        market_observers.add(new bitbay_observer("REP"));
//        market_observers.add(new bitbay_observer("PAY"));

        Thread thread = new Thread(Main::refresh_periodically);
        thread.setDaemon(true);
        thread.start();

        make_transactions();

        try { thread.join();  }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); }

    }
}
