import java.util.Random;

public class Main {

    private interface IComparison {
        public void sort(int[] array);
    }
    private static IComparison quick = array -> {
        quickSort(array, 0, array.length - 1);
    };
    private static IComparison shell = Main::shellSort;
    private static IComparison bubble = Main::bubbleSort;
    private static IComparison selection = Main::selectionSort;

    private static void comparison(int[] array, IComparison comparison) {
        long start = System.currentTimeMillis();
        comparison.sort(array);
        long finish = System.currentTimeMillis();
        long timeConsumedMillis = finish - start;
        System.out.println("Czas wykonnania - " + timeConsumedMillis);
    }

    private static void quickSort(int[] array, int n1, int n2) {
        if (n1 < n2) {
            int k = partition(array, n1, n2);
            quickSort(array, n1, k - 1);
            quickSort(array, k + 1, n2);
        }
    }

    private static int partition(int[] array, int n1, int n2) {
        int pivot = array[n1];
        int i = n1;
        for (int j = n1 + 1; j <= n2; j++)
            if (array[j] < pivot) {
                ++i;
                swap(array, i, j);
            }
        swap(array, n1, i);
        return i;
    }

    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    private static void shellSort(int[] array) {
        int j;
        for (int k = array.length / 2; k > 0; k /= 2) {
            for (int i = k; i < array.length; i++) {
                int buf = array[i];
                for (j = i; j >= k && array[j - k] > buf; j -= k) {
                    array[j] = array[j - k];
                }
                array[j] = buf;
            }
        }
    }

    private static void selectionSort(int[] array) {
        for (int i = 0; i < array.length; i++) {
            int min = array[i];
            int minId = i;
            for (int j = i + 1; j < array.length; j++) {
                if (array[j] < min) {
                    min = array[j];
                    minId = j;
                }
            }
            int buf = array[i];
            array[i] = min;
            array[minId] = buf;
        }
    }

    private static void bubbleSort(int[] array) {
        boolean flag = false;
        int buf;
        while (!flag) {
            flag = true;
            for (int i = 0; i < array.length - 1; i++) {
                if (array[i] > array[i + 1]) {
                    buf = array[i];
                    array[i] = array[i + 1];
                    array[i + 1] = buf;
                    flag = false;
                }
            }
        }
    }

    public static void main(String[] args) {
        Random random = new Random();
        int[] forQuick = new int[10000];
        for (int i = 0; i < forQuick.length; i++) {
            forQuick[i] = random.nextInt(10000);
        }
        comparison(forQuick, quick);
        int[] forBubble = new int[10000];
        for (int i = 0; i < forBubble.length; i++) {
            forBubble[i] = random.nextInt(10000);
        }
        comparison(forBubble, bubble);
        int[] forShell = new int[10000];
        for (int i = 0; i < forShell.length; i++) {
            forShell[i] = random.nextInt(10000);
        }
        comparison(forShell, shell);
        int[] forSelection = new int[10000];
        for (int i = 0; i < forSelection.length; i++) {
            forSelection[i] = random.nextInt(10000);
        }
        comparison(forSelection, selection);
    }
}
