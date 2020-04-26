package com.company;

public class InsertSort extends Sorting{

    public InsertSort() {
        super();
    }

    public InsertSort(int[] tab) {
        super(tab);
    }

    public void sortAll() {
        for(int i=1; i<tab.length; i++) {
            int elem = tab[i];
            int id = i - 1;

            while(id>=0 && elem<tab[id]) {
                tab[id+1]=tab[id];
                id--;
            }
            tab[id+1] = elem;
        }
    }
}
