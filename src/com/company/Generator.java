package com.company;

import java.util.Random;

public class Generator {

    private int n, lowerRange, upperRange;
    private int tab[];

    public Generator(int n, int lowerRange, int upperRange) {
        if(n<=0) this.n = 0;
        else this.n = n;
        this.lowerRange = lowerRange;
        this.upperRange = upperRange;

        this.tab = new int[n];
    }

    public void generateRandom() {
        Random generateRandomNumber=new Random();
        for(int i = 0; i < n; i++) {
            tab[i] = generateRandomNumber.nextInt(upperRange-lowerRange)+lowerRange;
        }
    }

    public int[] getTabCopy() {
        int[] copyTab = new int[n];
        for(int i = 0; i < n; i++) {
            copyTab[i] = copyTab[i];
            System.out.println(tab[i]);
        }
        return copyTab;
    }
}
