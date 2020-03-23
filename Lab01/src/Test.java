public class Test {

    public static void main(String[] args) {
        int[] arr0 = { 15, 9, 24, 2, 7, 71, 68, 13, 10, 52, 12, 14, 23, 85, 41 };
        int[] arr1 = { 15, 9, 24, 2, 7, 71, 68, 13, 10, 52, 12, 14, 23, 85, 41 };

        BubbleSort.sort(arr0);
        InsertSort.sort(arr1);

        System.out.println("bubble sort:");
        printArray(arr0);
        System.out.println("insert sort:");
        printArray(arr1);
    }

    private static void printArray(int[] arr) {
        for (int value : arr) System.out.print(value + " ");
        System.out.println();
    }

}
