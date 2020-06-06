import java.net.URL;
import java.net.URLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class JSONParser 
{
	private URL source;
	private String [] data;
	
	public JSONParser(URL source) {
		this.source = source;
		try {
			updateData();
		} 
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public String [] getData() {
		return data;
	}
	
	public void updateData() {
		try {
			URLConnection connection = source.openConnection();
			connection.addRequestProperty("User-Agent", "Mozilla");
			connection.connect();
			
			BufferedReader buffer = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			data = buffer.readLine().replaceAll("[:\\[\\]\\{\\}\"]", "").split(",");
		} 
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	
}
