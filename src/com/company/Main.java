package com.company;

public class Main {

    public static void main(String[] args) {

        int[] testArray = {5,7,3,8,2,4,6,7,8,9,0,3,4,-12,3,4,-3};
        int[] testArray2 = {5,7,3,8,2,4,6,7,8,9,0,3,4,-12,3,4,-3};
        int[] testArray3 = {5,7,3,8,2,4,6,7,8,9,0,3,4,-12,3,4,-3};
        int[] testArray4 = {5,7,3,8,2,4,6,7,8,9,0,3,4,-12,3,4,-3};
        MergeSort mSort = new MergeSort(testArray);
        InsertSort iSort = new InsertSort(testArray2);
        QuickSort qSort = new QuickSort(testArray3);

        System.out.println("MergeSort: ");

        mSort.sortAll();

        for (int e: testArray) {
            System.out.println(e);
        }

        System.out.println("InsertSort: ");

        iSort.sort();

        for (int e: testArray2) {
            System.out.println(e);
        }

        System.out.println("QuickSort: ");

        qSort.sortAll();

        for (int e: testArray3) {
            System.out.println(e);
        }

    }
}
