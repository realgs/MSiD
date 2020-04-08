import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class Comparison {
    private int listLength;

    public Comparison(int listLength) {
        this.listLength = listLength;
    }

    public Comparison() {
        this(10000);
    }

    public long getSortingTime(ArrayListSorter<Integer> sorter, ArrayList<Integer> listToSort) {
        ArrayList<Integer> copy = new ArrayList<>(listToSort);

        long time = System.currentTimeMillis();
        sorter.sort(copy);

        return System.currentTimeMillis() - time;
    }

    public void compareAlgorithms() {
        ArrayList<ArrayListSorter<Integer>> listOfAlgorithms = new ArrayList<>();

        BubbleSort<Integer> bubbleSort = new BubbleSort<>();
        listOfAlgorithms.add(bubbleSort);

        ShellSort<Integer> shellSort = new ShellSort<>();
        listOfAlgorithms.add(shellSort);

        InsertSort<Integer> insertSort = new InsertSort<>();
        listOfAlgorithms.add(insertSort);

        printResult(listOfAlgorithms);
    }

    private void printResult(ArrayList<ArrayListSorter<Integer>> algorithms) {
        ArrayList<Integer> listOfNumbers = createArrayList();
        ArrayList<MyPair> timeWithAlgorithm = new ArrayList<>(algorithms.size());

        for (ArrayListSorter<Integer> sorter : algorithms) {
            timeWithAlgorithm.add(new MyPair(sorter, getSortingTime(sorter, listOfNumbers)));
        }

        Collections.sort(timeWithAlgorithm);

        for (int i = 0; i < timeWithAlgorithm.size(); ++i) {
            System.out.print((i + 1) + ". " + timeWithAlgorithm.get(i).getAlgorithm().getClass().getName());
            System.out.println(" with time: " + timeWithAlgorithm.get(i).getSortTime() + " [ms]");
        }
    }

    private ArrayList<Integer> createArrayList() {
        Random random = new Random();
        ArrayList<Integer> list = new ArrayList<>(listLength);
        for (int i = 0; i < listLength; ++i) {
            list.add(random.nextInt(Integer.MAX_VALUE));
        }

        return list;
    }

    private static class MyPair implements Comparable<MyPair> {
        private ArrayListSorter<Integer> sortingAlgorithm;
        private long sortTime;

        MyPair(ArrayListSorter<Integer> sorter, long sortTime) {
            sortingAlgorithm = sorter;
            this.sortTime = sortTime;
        }

        ArrayListSorter<Integer> getAlgorithm() {
            return sortingAlgorithm;
        }

        long getSortTime() {
            return sortTime;
        }

        @Override
        public int compareTo(MyPair pair) {
            return Long.compare(this.sortTime, pair.sortTime);
        }
    }
}
