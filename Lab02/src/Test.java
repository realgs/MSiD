public class Test {

    public static void main(String[] args) {
        int[] arr0 = { 15, 9, 24, 2, 2, 7, 71, 68, 13, 10, 52, 71, 12, 14, 23, 85, 41 };
        int[] arr1 = { 15, 9, 24, 2, 2, 7, 71, 68, 13, 10, 52, 71, 12, 14, 23, 85, 41 };

        int[] arr2 = { 5, 4, 3, 2, 1};
        int[] arr3 = { 5, 4, 3, 2, 1};

        System.out.println("RANDOM");
        BubbleSort.sort(arr0);
        InsertSort.sort(arr1);

        System.out.println("bubble sort:");
        printArray(arr0);
        System.out.println("insert sort:");
        printArray(arr1);
        System.out.println();

        System.out.println("REVERSE ORDER");
        BubbleSort.sort(arr2);
        InsertSort.sort(arr3);

        System.out.println("bubble sort:");
        printArray(arr2);
        System.out.println("insert sort:");
        printArray(arr3);
        System.out.println();

        System.out.println("CORRECT ORDER");
        BubbleSort.sort(arr2);
        InsertSort.sort(arr3);

        System.out.println("bubble sort:");
        printArray(arr2);
        System.out.println("insert sort:");
        printArray(arr3);
    }

    private static void printArray(int[] arr) {
        for (int value : arr) System.out.print(value + " ");
        System.out.println();
    }

}