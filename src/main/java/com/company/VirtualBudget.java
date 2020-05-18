package com.company;

public class VirtualBudget {
    private double usd;
    private double eur;

    private double arbitrageGainUsd = 0.0;
    private double arbitrageGainEur = 0.0;
    //arbitraż uwzględnia jednoczesną wymianę, nie ma więc potrzeby przechowywania bitcoina i litecoina

    public VirtualBudget() {
        usd = 0.0;
        eur = 0.0;
    }

    public VirtualBudget(double startingUsd, double startingEur) {
        usd = startingUsd;
        eur = startingEur;
    }

    public double getCurrentUSD() {
        return usd;
    }

    public double getCurrentEUR() {
        return eur;
    }

    public void addGainUsd(double gainUsd, boolean fromArbitrage){
        usd+=gainUsd;
        if(fromArbitrage) arbitrageGainUsd+=gainUsd;
    }

    public void addGainEur(double gainEur, boolean fromArbitrage){
        usd+=gainEur;
        if(fromArbitrage) arbitrageGainEur+=gainEur;
    }

    public void printRaport() {
        System.out.println("Virtual budget");
        System.out.printf("account funds: \n USD: %.2f \n EUR: %.2f \n", usd, eur);
        System.out.printf("Gain (arbitrage): \n USD: %.2f \n EUR: %.2f \n", arbitrageGainUsd, arbitrageGainEur);
    }
}
