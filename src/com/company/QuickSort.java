package com.company;

import java.util.Random;

public class QuickSort implements Sorting{

    private int[] tab;

    public QuickSort() {
        this.tab=new int[]{};
    }

    public QuickSort(int[] tab) {
        this.tab=tab;
    }

    public void setTabToSort(int[] tab) {
        this.tab = tab;
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
