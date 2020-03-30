import java.util.Random;

public class SortingComparison {

    private interface IComparison {
        public void sort(int[] array);
    }



    private static void comparison(int[] array, IComparison comparison) {
        long start = System.currentTimeMillis();
        comparison.sort(array);
        long finish = System.currentTimeMillis();
        long timeConsumedMillis = finish - start;
        System.out.println("Sorting time : " + timeConsumedMillis);
    }

    private static IComparison bubble = SortingComparison::bubbleSort;
    private static IComparison insertSort = SortingComparison::insertSort;

    public static void bubbleSort(int[] array) {

        int temp;

        for (int i = array.length - 1; i > 0; i--) {
            for (int j = 0; j < i; j++) {
                if (array[j] > array[j + 1]) {
                    temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
            }
        }
    }

    public static void insertSort(int[] array) {

        for (int i = 1; i < array.length; ++i) {
            int key = array[i];
            int j = i - 1;

            while (j >= 0 && array[j] > key) {
                array[j+1] = array[j];
                j = j - 1;
            }
            array[j+1] = key;
        }
    }







    public static void main(String[] args) {
        Random random = new Random();

        int[] puzyrek = new int[10000];
        for (int i = 0; i < puzyrek.length; i++) {
            puzyrek[i] = random.nextInt(100000);
        }
        comparison(puzyrek, bubble);

        int[] wstawka = new int[10000];
        for (int i = 0; i < wstawka.length; i++) {
            wstawka[i] = random.nextInt(100000);
        }
        comparison(wstawka, insertSort);


    }
}



