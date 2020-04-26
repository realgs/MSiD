package com.company;

import java.util.Random;

public class QuickSort extends Sorting{

    public QuickSort() {
        super();
    }

    public QuickSort(int[] tab) {
        super(tab);
    }

    private void swap(int i, int j) {
        int tmp = tab[i];
        tab[i]=tab[j];
        tab[j]=tmp;
    }

    public void sort(int fst, int lst) {
        if(fst>=lst) return;

        Random generator=new Random();
        int i=fst;
        int j=lst;
        int pivot=tab[generator.nextInt(lst-fst)+fst];
        do{
            while(tab[i]<pivot) i++;
            while(tab[j]>pivot) j--;
            if(i<=j) {
                swap(i,j);
                i++;
                j--;
            }
        }while(i<=j);

        if(fst<j) sort(fst,j);
        if(i<lst) sort(i,lst);

    }

    public void sortAll() {
        sort(0, tab.length-1);
    }
}
