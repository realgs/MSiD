package com.company;

public class MergeSort extends Sorting{

    private int[] tmp;

    public MergeSort() {
        super();
        tmp = new int[]{};
    }

    public MergeSort(int[] tab) {
        super(tab);
        tmp = new int[tab.length];
    }

    public void setTabToSort(int[] tab) {
        super.setTabToSort(tab);
        tmp = new int[tab.length];
    }

    private void merge(int fst, int mid, int lst) {
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

    public void sort(int fst, int lst) {
        if(fst==lst) return;
        int mid=((lst+fst) / 2);
        sort(fst, mid);
        sort(mid+1, lst);
        merge(fst, mid, lst);
    }

    public void sortAll() {
        sort(0, tab.length-1);
    }
}
