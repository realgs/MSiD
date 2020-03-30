package sortingComparison;

import java.util.ArrayList;
import java.util.List;
import static java.util.stream.Collectors.toList;

import sorting.SortingAlgorithm;

public class SortingAlgorithmsComparator<T extends Comparable<T>> {
    ArrayList<SortMeasurer<T>> algorithms = new ArrayList<>();
    ArrayList<ArrayList<Long>> algorithmsResults = new ArrayList<>();

    public SortingAlgorithmsComparator(List<SortingAlgorithm<T>> algorithms) {
        for (SortingAlgorithm<T> algorithm : algorithms) {
            this.algorithms.add(new SortMeasurer<>(algorithm));
            algorithmsResults.add(new ArrayList<>());
        }
    }

    public void measureSortingTime(List<T> toSort) {
        for (int i = 0; i < algorithms.size(); i++) {
            SortMeasurer<T> measurer = algorithms.get(i);
            List<T> copy = toSort.stream().collect(toList());
            algorithmsResults.get(i).add(measurer.getSortingTime(copy));
        }
    }

    public ArrayList<Long> getAverageSortTime() {
        ArrayList<Long> results = new ArrayList<>(algorithmsResults.size());
        for (ArrayList<Long> list: algorithmsResults) {
            long average = 0;
            for (Long result : list) {
                average += result;
            }
            results.add(average / list.size());
        }
        return results;
    }

    public ArrayList<Long> getTotalSortTime() {
        ArrayList<Long> results = new ArrayList<>(algorithmsResults.size());
        for (ArrayList<Long> list: algorithmsResults) {
            long sum = 0;
            for (Long result : list) {
                sum += result;
            }
            results.add(sum);
        }
        return results;
    }
}
