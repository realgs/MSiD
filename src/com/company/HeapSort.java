package com.company;

public class HeapSort implements Sorting{

    private int tab[];

    public HeapSort() {
        this.tab = new int[]{};
    }

    public HeapSort(int[] tab) {
        this.tab = tab;
    }

    public void setTabToSort(int[] tab) {
        this.tab = tab;
    }

    private void swap(int i, int j) {
        int tmp = tab[i];
        tab[i]=tab[j];
        tab[j]=tmp;
    }

    private void heapify(int n, int rootId) {
        int largest = rootId;
        int left = 2 * rootId + 1;
        int right = 2 * rootId + 2;

        if (left < n && tab[left] > tab[largest])
            largest = left;

        if (right < n && tab[right] > tab[largest])
            largest = right;

        if (largest != rootId) {
            swap(largest, rootId);

            heapify(n, largest);
        }
    }

    public void sortAll(){
        int n = tab.length;

        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            swap(0, i);
            heapify(i, 0);
        }
    }
}
