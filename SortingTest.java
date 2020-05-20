import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class SortingTest {

    public void runTest() {
        BubbleSort<Integer> bubbleSort = new BubbleSort<>();
        printResult(bubbleSort);

        ShellSort<Integer> shellSort = new ShellSort<>();
        printResult(shellSort);
    }

    private void printResult(ArrayListSorter<Integer> sorter){
        if (checkCorrectness(sorter)) {
            System.out.println(sorter.getClass().getName() + " algorithm is working properly");
        } else {
            System.out.println(sorter.getClass().getName() + " algorithm isn't working properly");
        }
    }

    private boolean checkCorrectness(ArrayListSorter<Integer> sorter) {
        ArrayList<Integer> testList = createArrayList(10000);
        ArrayList<Integer> sortingAlgorithmList = new ArrayList<>(testList);

        Collections.sort(testList);
        sorter.sort(sortingAlgorithmList);

        return testList.equals(sortingAlgorithmList);
    }

    private static ArrayList<Integer> createArrayList(int size) {
        Random random = new Random();
        ArrayList<Integer> list = new ArrayList<>(size);

        for (int i = 0 ; i < size ; ++i) {
            list.add(random.nextInt(Integer.MAX_VALUE));
        }

        return list;
    }

}
