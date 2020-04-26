package com.company;

import org.junit.Test;

import static org.junit.Assert.assertArrayEquals;

public class SortingMethodsTests {

    @Test
    public void testSort1() {
        int[] tabQ= {5,8,2,6,14,1,3};
        int[] tabM= {5,8,2,6,14,1,3};
        int[] tabI= {5,8,2,6,14,1,3};
        int[] tabH= {5,8,2,6,14,1,3};

        MergeSort mSort = new MergeSort(tabM);
        InsertSort iSort = new InsertSort(tabI);
        QuickSort qSort = new QuickSort(tabQ);
        HeapSort hSort = new HeapSort(tabH);

        mSort.sortAll();
        iSort.sortAll();
        qSort.sortAll();
        hSort.sortAll();

        int[] tmp={1,2,3,5,6,8,14};

        assertArrayEquals(tmp, tabQ);
        assertArrayEquals(tmp, tabM);
        assertArrayEquals(tmp, tabI);
        assertArrayEquals(tmp, tabH);
    }

    @Test
    public void testSort2() {
        int[] tabQ= {3,3,3,2,2,3,3};
        int[] tabM= {3,3,3,2,2,3,3};
        int[] tabI= {3,3,3,2,2,3,3};
        int[] tabH= {3,3,3,2,2,3,3};

        MergeSort mSort = new MergeSort(tabM);
        InsertSort iSort = new InsertSort(tabI);
        QuickSort qSort = new QuickSort(tabQ);
        HeapSort hSort = new HeapSort(tabH);

        mSort.sortAll();
        iSort.sortAll();
        qSort.sortAll();
        hSort.sortAll();

        int[] tmp= {2,2,3,3,3,3,3};

        assertArrayEquals(tmp, tabQ);
        assertArrayEquals(tmp, tabM);
        assertArrayEquals(tmp, tabI);
        assertArrayEquals(tmp, tabH);
    }


}
