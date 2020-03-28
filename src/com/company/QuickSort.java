package com.company;

import java.util.Random;

public class QuickSort {

    private int[] tab;

    public QuickSort(int[] tab) {
        this.tab=tab;
    }

    public void swap(int i, int j) {
        int tmp = tab[i];
        tab[i]=tab[j];
        tab[j]=tmp;
    }

    public void sort(int fst, int lst) {
        if(fst>=lst) return;

        Random losowanie=new Random();
        int i=fst;
        int j=lst;
        int pivot=tab[losowanie.nextInt(lst-fst)+fst];
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
