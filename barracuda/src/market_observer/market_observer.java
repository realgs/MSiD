package market_observer;

public abstract class market_observer
{
    float bid_price = 0, ask_price = 0;
    private String currency, name;

    market_observer(String currency, String name)
    {
        this.currency = currency;
        this.name = name;
    }
    public float bid_price(){ return bid_price; }
    public float ask_price(){ return ask_price; }
    public float spread(){ return (ask_price - bid_price) / bid_price;}

    public void print_status()
    {
        System.out.println
        (
            currency + " @ " +
            name + ": bid = " +
            bid_price + ", ask = " +
            ask_price + ", spread = " +
            String.format("%.02f", 100 * spread()) + "%"
        );
    }

    public abstract void update_data();
}
