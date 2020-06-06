public class Offer
{
	private double price;
	private double ammount;
	
	public Offer() {
		price = 0;
		ammount = 0;
	}
	
	public Offer(double price, double ammount) {
		this.price = price;
		this.ammount = ammount;
	}
	
	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public double getAmmount() {
		return ammount;
	}

	public void setAmmount(double ammount) {
		this.ammount = ammount;
	}
	
	@Override
	public String toString() {
		return String.format("[CENA: %-15.2f ILOSC: %-12.8f]", price, ammount);
	}
	
}
