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
        System.out.println("Sorting time of algorithm: " + timeConsumedMillis);
    }

    private static IComparison bubbleS = SortingComparison::bubbleSort;
    private static IComparison insertS = SortingComparison::insertSort;
    private static IComparison selectionS = SortingComparison::selectionSort;
    private static IComparison quickS = array -> {
        Quicksort(array, 0, array.length - 1);
    };


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


    public static void selectionSort(int[] array){
        for (int i = 0; i < array.length - 1; i++)
        {
            int ind = i;
            for (int j = i + 1; j < array.length; j++){
                if (array[j] < array[ind]){
                    ind = j;
                }
            }
            int smallerN = array[ind];
            array[ind] = array[i];
            array[i] = smallerN;
        }
    }

    public static int partition(int[] array, int low, int high) {
        Random random = new Random();

        int pivot = random.nextInt(array.length);
        int i = (low - 1);

        for (int j = low; j < high; j++) {
            if (array[j] < pivot) {
                i++;

                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }

        }

        int temp = array[i + 1];
        array[i + 1] = array[high];
        array[high] = temp;

        return i + 1;


    }

    public static void Quicksort(int[] array, int low, int high){

        if(low<high) {

            int partitionIndex = partition(array, low, high);
            Quicksort(array,low, partitionIndex - 1);
            Quicksort(array, partitionIndex + 1, high);

        }
    }








    public static void main(String[] args) {
        Random random = new Random();
        System.out.println();
        System.out.println("BubbleSort");
        int[] puzyrek = new int[20000];
        for (int i = 0; i < puzyrek.length; i++) {
            puzyrek[i] = random.nextInt(20000);
        }
        comparison(puzyrek, bubbleS);
        System.out.println();

        System.out.println("InsertSort");
        int[] wstawka = new int[20000];
        for (int i = 0; i < wstawka.length; i++) {
            wstawka[i] = random.nextInt(20000);
        }
        comparison(wstawka, insertS);
        System.out.println();

        System.out.println("SelectionSort");
        int[] wybor = new int[20000];
        for (int i = 0; i < wybor.length; i++) {
            wybor[i] = random.nextInt(20000);
        }
        comparison(wybor, selectionS);
        System.out.println();

        System.out.println("QuickSort");
        int[] bystrij = new int[20000];
        for (int i = 0; i < bystrij.length; i++) {
            bystrij[i] = random.nextInt(20000);
        }
        comparison(bystrij,quickS);




    }
}



