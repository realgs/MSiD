package main;

import market_observer.*;

import java.time.*;
import java.util.ArrayList;

public class Main
{
    private static ArrayList<market_observer> market_observers = new ArrayList<market_observer>();
    private static int refresh_interval;

    private static void refresh()
    {
        System.out.println("\n----- Status for " + Instant.now() + " -----");
        for ( market_observer observer: market_observers )
        {
            observer.update_data();
            observer.print_status();
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
        refresh_interval = 4000;

        market_observers.add(new bitbay_observer("BTC"));
        market_observers.add(new bybit_observer("BTC"));
        market_observers.add(new bitfinex_observer("BTC"));
//        market_observers.add(new whitebit_observer("BTC"));
//        market_observers.add(new bitbay_observer("LTC"));
//        market_observers.add(new bitbay_observer("LSK"));
//        market_observers.add(new bitbay_observer("GAME"));
//        market_observers.add(new bitbay_observer("REP"));
//        market_observers.add(new bitbay_observer("PAY"));


        Thread thread = new Thread(Main::refresh_periodically);
        thread.setDaemon(true);
        thread.start();
        try { thread.join();  }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }
}
