package com.company;

import java.util.ArrayList;

public class SortingComparison {

    public static double timepiece(Sorting sortingMethod, int tabToSort[]) {
        long time, startTime, endTime;
        sortingMethod.setTabToSort(tabToSort);
        startTime=System.nanoTime();
        sortingMethod.sortAll();
        endTime = System.nanoTime();
        time=(endTime-startTime)/10000;
        return (double)time/100;
    }

    public static ArrayList<Double> comparison(ArrayList<Sorting> sortMethods, Generator numberGenerator){
        ArrayList<Double> timeList = new ArrayList<>();
        for(Sorting method : sortMethods) {
            timeList.add(timepiece(method, numberGenerator.getTabCopy()));
        }
        return timeList;
    }
}
