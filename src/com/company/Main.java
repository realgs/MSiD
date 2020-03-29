package com.company;

import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {

        int n = 100000, lowerRange = -100, upperRange = 100;
        ArrayList<Sorting> sortingMethodsList = new ArrayList<>();
        MergeSort mSort = new MergeSort();
        InsertSort iSort = new InsertSort();
        QuickSort qSort = new QuickSort();
        HeapSort hSort = new HeapSort();
        Generator numberGenerator = new Generator(n, lowerRange, upperRange);

        numberGenerator.generateRandom();

        sortingMethodsList.add(mSort);
        sortingMethodsList.add(iSort);
        sortingMethodsList.add(qSort);
        sortingMethodsList.add(hSort);

        ArrayList<Long> results = SortingComparison.comparison(sortingMethodsList, numberGenerator);

        for(int i=0; i < sortingMethodsList.size(); i++) {
            System.out.println(results);
        }
    }
}
