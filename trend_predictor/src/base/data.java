package base;

public class data
{
    private float price;
    private float volume;

    public data()
    {
        this.price = 0f;
        this.volume = 0f;
    }

    public data(float price, float volume)
    {
        this.price = price;
        this.volume = volume;
    }

    public float price() { return price; }
    public float volume() { return volume; }
}
