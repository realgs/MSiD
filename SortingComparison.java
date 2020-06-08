import java.util.ArrayList;
import java.util.Random;

public class SortingComparison {
    private int length;

    public SortingComparison(){
        this.length = 10000;
    }

    public SortingComparison(int length){
        this.length = length;
    }

    public void comparison(){
        ArrayList<Integer> list = createList();
        ArrayList<ListSorter<Integer>> listSorters = new ArrayList<>();

        listSorters.add(new InsertSort<>());
        listSorters.add(new ShellSort<>());
        listSorters.add(new HeapSort<>());
        listSorters.add(new QuickSort<>());

        for (ListSorter<Integer> sorter : listSorters){
            long time = getSortingTime(sorter, list);
            printResult(sorter, time);
        }
    }

    public long getSortingTime(ListSorter<Integer> algorithm, ArrayList<Integer> list){
        ArrayList<Integer> copyOfList = new ArrayList<>(list);
        long time = System.currentTimeMillis();

        algorithm.sort(copyOfList);

        return System.currentTimeMillis() - time;
    }

    private ArrayList<Integer> createList(){
        ArrayList<Integer> arrayList = new ArrayList<>();
        Random rand = new Random();

        for (int i = 0; i < length; i++){
            arrayList.add(rand.nextInt(Integer.MAX_VALUE));
        }

        return arrayList;
    }

    private void printResult(ListSorter<Integer> algorithm, long time){
        System.out.println(algorithm.toString() + ": " + time + " ms");
    }
}
