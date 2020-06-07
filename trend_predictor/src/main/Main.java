package main;

import base.data;
import base.history_provider;
import org.knowm.xchart.*;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.Random;

public class Main
{
    private static Random generator = new Random();
    private static history_provider btc_provider = new history_provider("bitcoin");
    private static history_provider ltc_provider = new history_provider("litecoin");
    private static history_provider eth_provider = new history_provider("ethereum");

    public static void draw_chart(OHLCChart chart, ArrayList<data> historical, ArrayList<data> predicted, String date_from, String date_to, String caption)
    {
        ArrayList<Date> xData = new ArrayList<Date>();
        ArrayList<Float> openData = new ArrayList<Float>();
//        ArrayList<Float> highData = new ArrayList<Float>();
//        ArrayList<Float> lowData = new ArrayList<Float>();
        ArrayList<Float> closeData = new ArrayList<Float>();
        ArrayList<Float> volumeData = new ArrayList<Float>();

        try
        {
            SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy"); // 23-03-2015
            SimpleDateFormat reversed_formatter = new SimpleDateFormat("yyyy-MM-dd"); // 2015-03-23
            Date startDate = formatter.parse(date_from);
            Date endDate = formatter.parse(date_to);
            LocalDate start = startDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
            LocalDate end = endDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

            int change_index = 0;
            for (LocalDate date = start; !date.isAfter(end); date = date.plusDays(1))
            {
                xData.add(reversed_formatter.parse(date.toString()));
            }

        }
        catch (ParseException e) { e.printStackTrace(); }

        xData.add(xData.get(xData.size() - 1));

        openData.add(historical.get(0).price());
        historical.forEach(x ->
        {
            openData.add(x.price());
            closeData.add(x.price());
            volumeData.add(x.volume());
        });
        predicted.forEach(x ->
        {
            openData.add(x.price());
            closeData.add(x.price());
            volumeData.add(x.volume());
        });

        openData.remove(openData.size() - 1);

        chart.addSeries(caption, xData, openData, closeData, openData, closeData, volumeData);

        System.out.println("------------------");
        System.out.println(caption);
        System.out.println("FROM: " + date_from);
        historical.forEach(x -> System.out.println("price: " +  x.price() + "\tvolume: " + x.volume()));
        predicted.forEach(x -> System.out.println("price: " +  x.price() + "\tvolume: " + x.volume()));
        System.out.println("TO: " + date_to);
    }

    private static ArrayList<data> values_to_changes(ArrayList<data> values)
    {
        ArrayList<data> changes = new ArrayList<data>();

        for (int i = 1; i < values.size(); i++)
        {
            float price_change = (values.get(i).price() - values.get(i - 1).price()) / values.get(i - 1).price();
            float volume_change = (values.get(i).volume() - values.get(i - 1).volume()) / values.get(i - 1).volume();
            changes.add(new data(price_change, volume_change));

//        changes.forEach((x)->System.out.printf("p:\t%.2f%%\tv:\t%.2f%%\n", + x.price() * 100, x.volume() * 100));
        }

        return changes;
    }

    static ArrayList<ArrayList<data>> generate_prediction(String currency, String base_date_from, String base_date_to, String prediction_end_date)
    {
        ArrayList<ArrayList<data>> predictions = new ArrayList<ArrayList<data>>();
        ArrayList<data> historical_data;

        switch (currency)
        {
            case "LTC":
                historical_data = ltc_provider.provide_data(base_date_from, base_date_to);
                break;
            case "ETH":
                historical_data = eth_provider.provide_data(base_date_from, base_date_to);
                break;
            default: // BTC
                historical_data = btc_provider.provide_data(base_date_from, base_date_to);
        }

        data last_data = historical_data.get(historical_data.size() - 1);
        for (int i = 0; i < 100; i++)
            predictions.add(generate_prediction(values_to_changes(historical_data), last_data, base_date_to, prediction_end_date));

        int predictions_size = predictions.size();
        int prediction_size = predictions.get(0).size();
        ArrayList<data> average_prediction = new ArrayList<data>();
        ArrayList<data> median_prediction = new ArrayList<data>();
        ArrayList<data> standard_deviations = new ArrayList<data>();

        for (int j = 0; j < prediction_size; j++)
        {
            ArrayList<Float> prices = new ArrayList<Float>();
            ArrayList<Float> volumes = new ArrayList<Float>();
            float average_price = 0, average_volume = 0;
            float price_deviation = 0, volume_deviation = 0;

            for (int i = 0; i < predictions_size; i++)
            {
                prices.add(predictions.get(i).get(j).price());
                volumes.add(predictions.get(i).get(j).volume());

                average_price += predictions.get(i).get(j).price();
                average_volume += predictions.get(i).get(j).volume();
            }

            prices.sort(Comparator.naturalOrder());
            volumes.sort(Comparator.naturalOrder());

            if(predictions_size % 2 == 0)
            {
                float median_price = (prices.get(prices.size() / 2) + prices.get(prices.size() / 2 - 1)) / 2;
                float median_volume = (volumes.get(volumes.size() / 2) + volumes.get(volumes.size() / 2 - 1)) / 2;
                median_prediction.add(new data(median_price, median_volume));
            }
            else
            {
                float median_price = prices.get(prices.size() / 2);
                float median_volume = volumes.get(volumes.size() / 2);
                median_prediction.add(new data(median_price, median_volume));
            }

            average_price /= predictions_size;
            average_volume /= predictions_size;

            for (ArrayList<data> prediction : predictions)
            {
                price_deviation += (prediction.get(j).price() - average_price) * (prediction.get(j).price() - average_price);
                volume_deviation += (prediction.get(j).volume() - average_volume) * (prediction.get(j).volume() - average_volume);
            }

            price_deviation /= (predictions_size - 1);
            volume_deviation /= (predictions_size - 1);
            price_deviation = (float) Math.sqrt(price_deviation);
            volume_deviation = (float) Math.sqrt(volume_deviation);

            standard_deviations.add(new data(price_deviation, volume_deviation));
            average_prediction.add(new data(average_price,  average_volume));
        }

        OHLCChartBuilder chart_builder =  new OHLCChartBuilder();
        chart_builder.height = 600;
        chart_builder.width =  800;
        chart_builder.title = currency + " from " + base_date_from + " to " + prediction_end_date;
        OHLCChart chart = new OHLCChart(chart_builder);

//        draw_chart(chart, historical_data, predictions.get(0), base_date_from, prediction_end_date, "single");
        draw_chart(chart, historical_data, average_prediction, base_date_from, prediction_end_date, "average");
//        draw_chart(chart, historical_data, median_prediction, base_date_from, prediction_end_date, "median");

        new SwingWrapper(chart).displayChart();

        System.out.println("standard deviations: ");
        standard_deviations.forEach(deviation -> System.out.println("price: " +  deviation.price() + "\tvolume: " + deviation.volume()));

        return predictions;
    }

    public static ArrayList<data> generate_prediction(ArrayList<data> base, data last, String date_from, String date_to) // 23-03-2015
    {
        ArrayList<data> prediction = new ArrayList<data>();

        try
        {
            SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy"); // 23-03-2015
            SimpleDateFormat reversed_formatter = new SimpleDateFormat("yyyy-MM-dd"); // 2015-03-23
            Date startDate = formatter.parse(date_from);
            Date endDate = formatter.parse(date_to);
            LocalDate start = startDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
            LocalDate end = endDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

            int change_index = 0;
            for (LocalDate date = start; !date.isAfter(end); date = date.plusDays(1))
            {
                change_index = generator.nextInt(base.size());
                float next_price = last.price() * (base.get(change_index).price() + 1);
                float next_volume = last.volume() * (base.get(change_index).volume() + 1);
                last = new data(next_price, next_volume);
                prediction.add(last);
            }

        }
        catch (ParseException e) { e.printStackTrace(); }

        return prediction;
    }

    public static void main(String[] args) throws IOException
    {
        generate_prediction("BTC", "23-03-2015", "28-03-2015", "30-04-2015");
    }
}
