package sorting;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < 15; i++) {
            list.add(random.nextInt(100));
        }
        System.out.println(list);
        System.out.println(SortingMethods.quicksort(list));

    }
}
