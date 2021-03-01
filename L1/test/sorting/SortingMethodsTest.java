package sorting;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class SortingMethodsTest {

   @Test
    void sortTest() {
       Random random = new Random();
       for (int i = 0; i < 100; i++) {
           List<Integer> list = new ArrayList<>();
           for (int j = 0; j < 100; j++)
               list.add(random.nextInt(Integer.MAX_VALUE));
           List<Integer> expected = new ArrayList<>(list);
           List<Integer> quicksort = new ArrayList<>(list);
           expected.sort(Integer::compareTo);
           assertEquals(SortingMethods.selectionSort(list), expected);
           assertEquals(SortingMethods.quicksort(quicksort), expected);
       }
   }
}