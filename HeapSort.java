public class HeapSort {

    void sort(int [] tab) {
        for (int i = tab.length / 2 - 1; i >= 0; i--) {
            heapify(tab, tab.length, i);
        }

        for (int i = tab.length - 1; i >= 0; i--) {
            int temp = tab[0];

            tab[0] = tab[i];
            tab[i] = temp;
            heapify(tab, i, 0);
        }


    }

    private void heapify(int tab[], int n, int i) {
        int largest = i, left = 2 * i + 1, right = 2 * i + 2;

        if (left < n && tab[left] > tab[largest]) {
            largest = left;
        }

        if (right < n && tab[right] > tab[largest]) {
            largest = right;
        }

        if (largest != i) {
            int swap = tab[i];

            tab[i] = tab[largest];
            tab[largest] = swap;

            heapify(tab, n, largest);
        }
    }
}