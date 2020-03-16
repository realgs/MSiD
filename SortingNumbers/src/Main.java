public class Main {

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
        int[] bubbleArray = new int[]{6, 4, 2, 7, 124, 64, 125, 1, 2, 35, 2, 32};
        bubbleSort(bubbleArray);
        for (int value : bubbleArray) {
            System.out.print(value + " ");
        }
        System.out.println();

        int[] selectionArray = new int[]{2, 4, 1, 6, 7, 1, 5, 42, 25, 124, 64};
        selectionSort(selectionArray);
        for (int value : selectionArray) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
}
