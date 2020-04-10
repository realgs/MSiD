import java.util.ArrayList;
import java.util.Random;

public class Test {

    public static void main(String[] args) {
        ArrayList<Integer> list0 = new ArrayList<>(randomIntegerArrayList(10000));

        BubbleSort<Integer> integerBubbleSort = new BubbleSort<>();
        InsertSort<Integer> integerInsertSort = new InsertSort<>();
        MergeSort<Integer> integerMergeSort = new MergeSort<>();
        QuickSort<Integer> integerQuickSort = new QuickSort<>();

        Comparison<Integer> integerComparison = new Comparison<>();

        System.out.println(integerBubbleSort + " " + integerComparison.executionTime(integerBubbleSort, list0));
        System.out.println(integerInsertSort + " " + integerComparison.executionTime(integerInsertSort, list0));
        System.out.println(integerMergeSort + " " + integerComparison.executionTime(integerMergeSort, list0));
        System.out.println(integerQuickSort + " " + integerComparison.executionTime(integerQuickSort, list0));
        System.out.println();

    }

    private static void printArrayList(ArrayList list) {
        for (Object elem : list) System.out.print(elem + " ");
        System.out.println();
    }

    private static ArrayList<Integer> randomIntegerArrayList(int size) {
        Random r = new Random();
        ArrayList<Integer> list = new ArrayList<>();
        for (int i = 0; i < size; ++i)
            list.add(r.nextInt(100000));
        return list;
    }
}