package com.company;

public abstract class Sorting {

    protected int tab[];

    public Sorting() {
        tab = new int[]{};
    }

    public Sorting(int[] tab) {
        this.tab = tab;
    }

    abstract void sortAll();

    public void setTabToSort(int tab[]) {
        this.tab = tab;
    };


    public boolean isTabSort() {
        int current, next;

        if(tab.length == 0 || tab.length == 1) return true;

        current = tab[0];

        for(int i=0; i < tab.length; i++) {
            next = tab[i];

            if(next < current) {
                return false;
            }

            current = next;
        }

        return true;
    }


    public void print() {
        System.out.println(this.getClass().getName());
        for(int i = 0; i < tab.length; i++) {
            System.out.print(tab[i] + ", ");
        }
    }
}
