public class Main {

    private static void quickSort(int[] array, int n1, int n2) {
        if (n1 < n2) {
            int k = partition(array, n1, n2);
            quickSort(array, n1, k-1);
            quickSort(array, k+1, n2);
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
        int[] quick = new int[]{6, 4, 2, 7, 124, 64, 125, 1, 2, 35, 2, 32};
        quickSort(quick, 0, quick.length - 1);
        for (int value : quick) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
}
