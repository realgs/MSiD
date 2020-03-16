package com.company;

import java.util.ArrayList;

public class MergeSort {

    private int[] tab;
    private int[] tmp;

    public MergeSort(int[] tab) {
        this.tab = tab;
        tmp = new int[tab.length];
    }

    private void merge(int fst, int mid, int lst)
    {
        for (int i=fst; i<=lst; i++) tmp[i]=tab[i];
        int idRight=mid+1,idLeft=fst,idTmpTab=fst;
        while (idLeft<=mid&&idRight<=lst) {
            if (tmp[idLeft]<tmp[idRight])	{
                tab[idTmpTab++]=tmp[idLeft++];
            }
            else{
                tab[idTmpTab++]=tmp[idRight++];
            }
        }
        while (idLeft<=mid) tab[idTmpTab++]=tmp[idLeft++];
    }

    public void sort(int fst, int lst)
    {
        if(fst==lst) return;
        int mid=((lst+fst) / 2);
        sort(fst, mid);
        sort(mid+1, lst);
        merge(fst, mid, lst);
    }

    public void sortAll()
    {
        sort(0, tab.length-1);
    }
}
