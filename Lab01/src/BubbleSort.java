public class BubbleSort {

    static void sort (int[] arr) {
        int n = arr.length;
        int tmp;
        for (int i = 1; i < n; ++i)
            for (int j = 1; j < n - i; ++j)
                if (arr[j - 1] > arr[j]) {
                    tmp = arr[j - 1];
                    arr[j - 1] = arr[j];
                    arr[j] = tmp;
                }
    }

}
