import org.json.simple.parser.ParseException;
import java.io.IOException;

public class Main {

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

    private static void refresh() {
        while (true) {
            try {
                try {
                    Observer.getData("BTC", "");
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
