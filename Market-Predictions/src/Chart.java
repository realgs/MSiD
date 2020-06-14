import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.stage.Stage;
import org.json.simple.parser.ParseException;
import java.io.IOException;
import java.util.ArrayList;
public class Chart extends Application {

    @Override public void start(Stage stage) throws ParseException, java.text.ParseException, IOException {
        stage.setTitle("Line Chart Sample");
        final CategoryAxis xAxis = new CategoryAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Date");
        final LineChart<String,Number> lineChart =
                new LineChart<String,Number>(xAxis,yAxis);

        lineChart.setTitle("Stock Monitoring");
        ArrayList<History> list = History.predict100("3-05-2020","30-05-2020", "20-06-2020");
        ArrayList<History> future = History.predict("3-05-2020","30-05-2020", "20-06-2020");
        ArrayList<History> history = History.makelist("3-05-2020","30-05-2020");
        XYChart.Series pricesH = new XYChart.Series();
        pricesH.setName("History Prices");
        XYChart.Series pricesF = new XYChart.Series();
        pricesF.setName("Future Prices ");
        XYChart.Series pricesF1 = new XYChart.Series();
        pricesF1.setName("Future Prices ");
        XYChart.Series capsH = new XYChart.Series();
        capsH.setName("History Market capacity");
        XYChart.Series capsF = new XYChart.Series();
        capsF.setName("Future Market capacity");
        XYChart.Series capsF1 = new XYChart.Series();
        capsF1.setName("Future Market capacity");
        XYChart.Series volumesH = new XYChart.Series();
        volumesH.setName("History Volumes");
        XYChart.Series volumesF = new XYChart.Series();
        volumesF.setName("Future Volumes");
        XYChart.Series volumesF1 = new XYChart.Series();
        volumesF1.setName("Future Volumes");
        for(int i=0; i<history.size(); i++){
            pricesH.getData().add(new XYChart.Data(history.get(i).getDate(), history.get(i).getPrice()));
            capsH.getData().add(new XYChart.Data(history.get(i).getDate(), history.get(i).getMarket_cap()));
            volumesH.getData().add(new XYChart.Data(history.get(i).getDate(), history.get(i).getVolume()));
        }
        for(int i=0; i<list.size(); i++){
            pricesF.getData().add(new XYChart.Data(list.get(i).getDate(), list.get(i).getPrice()));
            capsF.getData().add(new XYChart.Data(list.get(i).getDate(), list.get(i).getMarket_cap()));
            volumesF.getData().add(new XYChart.Data(list.get(i).getDate(), list.get(i).getVolume()));
        }
        for(int i=0; i<future.size(); i++){
            pricesF1.getData().add(new XYChart.Data(future.get(i).getDate(), future.get(i).getPrice()));
            capsF1.getData().add(new XYChart.Data(future.get(i).getDate(), future.get(i).getMarket_cap()));
            volumesF1.getData().add(new XYChart.Data(future.get(i).getDate(), future.get(i).getVolume()));
        }
           Scene scene  = new Scene(lineChart,800,600);
        lineChart.getData().addAll(pricesH, pricesF, pricesF1);

        stage.setScene(scene);
        stage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }
}