package market_observer;

public abstract class market_observer
{
    float bid_price = 0, ask_price = 0, bid_amount = 0, ask_amount = 0;
    private float commission_rate = 0.005f;
    private String currency, name;

    market_observer(String currency, String name, float commission_rate)
    {
        this.currency = currency;
        this.name = name;
        this.commission_rate = commission_rate;
    }

    public float bid_price(){ return bid_price; }
    public float ask_price(){ return ask_price; }
    public float bid_amount(){ return bid_amount; }
    public float ask_amount(){ return ask_amount; }
    public float spread(){ return (ask_price - bid_price) / bid_price;}

    public void print_status()
    {
        System.out.println
        (
            currency + " @ " +
            name + ": bid = " +
            bid_amount + " ✖️ " + bid_price + ", ask = " +
            ask_amount + " ✖️ " + ask_price + ", spread = " +
            String.format("%.02f", 100 * spread()) + "%"
        );
    }

    public abstract void update_data();
}
