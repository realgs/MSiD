public class Main {

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
        int[] shell = new int[]{6, 4, 2, 7, 124, 64, 125, 1, 2, 35, 2, 32};
        shellSort(shell);
        for (int value : shell) {
            System.out.print(value + " ");
        }
        System.out.println();

    }
}
