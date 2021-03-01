
import java.util.*;
public class Sort1{
    private int tab[];
    private int lthread;
    private int zakres;
    public Sort1(int size,int lthread,int zakres) {
        tab=new int[size];
        this.lthread=lthread;
        if (lthread>Runtime.getRuntime().availableProcessors()) {
            lthread=Runtime.getRuntime().availableProcessors();
        }

        Random r=new Random();
        for (int i=0;i<size;i++) {
            tab[i]=r.nextInt(zakres)+1;
        }
        int [][] dtab=new int [lthread] [];
        for (int i=0;i<lthread-1;i++) {
            dtab[i]=new int[size/lthread];
        }
        int it=0;
        int roz=size-size/lthread*(lthread-1);
        dtab[lthread-1]=new int[roz];
        for (int i=0;i<lthread-1;i++) {
            for (int j=0;j<size/lthread;j++) {
                dtab[i][j]=tab[it];
                it++;
            }
        }
        for (int i=0;i<roz;i++) {
            dtab[lthread-1][i]=tab[it];
            it++;
        }
        Computer[] tabThread=new Computer [lthread];
        for (int i=0;i<lthread;i++) {
            tabThread[i]=new Computer (dtab[i]);
        }
        for (int i=0;i<lthread;i++) {
            tabThread[i].start();
            try {
                tabThread[i].join();
            } catch (InterruptedException e) {

            }
        }
        int[] tabFinal=new int[2];
        //System.out.println(tabFinal.length);

        for (int i=0;i<lthread;i++) {
            tabFinal=mergeAll(tabThread[0].getTab(),tabThread[i].getTab());
        }
        tab=tabFinal;


    }
    private int[] mergeAll(int[] tabL,int[] tabP) {
        int[] tabW=new int[tabL.length+tabP.length];
        int bl=0;
        int br=0;

        for (int i=0;i<tabW.length;i++) {
            if ((bl<tabL.length)&&(br<tabL.length)) {
                if (tabL[bl]<tabP[br]) {
                    tabW[i]=tabL[bl];
                    bl++;
                }
                else
                {
                    tabW[i]=tabP[br];
                    br++;
                }
            }
            else if (bl<tabL.length) {
                tabW[i]=tabL[bl];
                bl++;
            }
            else if (br<tabP.length) {
                tabW[i]=tabP[br];
                br++;
            }

        }
        return tabW;

    }
    public void showArray() {
        for (int i=0;i<tab.length;i++) {
            System.out.println(tab[i]);
        }
    }

}
class Computer extends Thread{
    private int [] tab;
    public Computer (int[] tab) {
        this.tab=tab;
    }
    public int[] getTab() {
        return tab;
    }
    private void mergesort (int[] tab) {

        if (tab.length>1) {
            int[] l=makeLeft(tab);
            int[] r=makeRight(tab);
            mergesort(l);
            mergesort(r);
            merge(tab,l,r);
        }


    }
    private int[] makeLeft(int[] tabP) {

        int end=tabP.length/2;
        int [] ntab=new int [end];
        for (int i=0;i<end;i++) {
            ntab[i]=tabP[i];

        }
        return ntab;
    }
    private int[] makeRight(int[] tabP) {

        int begin=tabP.length/2;
        int size=tabP.length-begin;
        int [] ntab=new int [size];
        for (int i=0;i<size;i++) {
            ntab[i]=tabP[begin++];

        }
        return ntab;
    }
    private void merge(int[] tabW,int[] tabL,int[] tabP) {
        int bl=0;
        int br=0;
        for (int i = 0; i < tabW.length; i++) {
            if (br >= tabP.length || (bl < tabL.length && tabL[bl] <= tabP[br])) {
                tabW[i] = tabL[bl];
                bl++;
            } else {
                tabW[i] = tabP[br];
                br++;
            }
        }


    }
    public void run() {
        mergesort(tab);

    }

}
class Tester{
    public static void main(String[] args) {
        long time1=System.currentTimeMillis();
        Sort1 m=new Sort1(100000,2,100000);
        long time2=System.currentTimeMillis()-time1;
        System.out.println("It takes "+time2+" to sort given array");

        //m.showArray();
    }
}
