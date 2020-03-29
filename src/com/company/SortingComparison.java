package com.company;

import java.util.ArrayList;

public class SortingComparison {

    public static long timepiece(Sorting sortingMethod, int tabToSort[]) {
        long time, startTime, endTime;
        sortingMethod.setTabToSort(tabToSort);
        startTime=System.nanoTime();
        sortingMethod.sortAll();
        endTime = System.nanoTime();
        time=(endTime-startTime+5000)/10000;
        return time;
    }

    public static ArrayList<Long> comparison(ArrayList<Sorting> sortMethods, Generator numberGenerator){
        ArrayList<Long> timeList = new ArrayList<>();
        for(Sorting method : sortMethods) {
            timeList.add(timepiece(method, numberGenerator.getTabCopy()));
        }
        return timeList;
    }
}
