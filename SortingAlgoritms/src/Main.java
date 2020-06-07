import SortingAlgorithms.InsertionSort;
import SortingAlgorithms.MergeSort;
import SortingAlgorithms.QuickSort;
import SortingAlgorithms.SelectionSort;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class Main {
    public static void main(String args[]) {
        List<Integer> list_integers = new ArrayList<>();
        Integer[] tab = {123, 12, 122, 34, 34, -12, 4, 127, 42, 6, 5, 8, 0, 8, 5, 6, 8, 9, 4, 7, 56, 8, 5, 76, 3, 6, 3, 6, 4, 6, 3, 6, 3, 6, 4, 3, 34535};
        Collections.addAll(list_integers, tab);

        List<Double> list_doubles = new ArrayList<>();
        Double[] tab2 = {1.0, 3.5, 12.1, 3.4, 1.1, 32.1};
        Collections.addAll(list_doubles, tab2);

        List<String> list_strings = new ArrayList<>();
        String[] strings = {"kot", "pies", "zając", "krowa", "biedronka", "moj_brat_michal"};
        Collections.addAll(list_strings, strings);


        List<Character> characters = new ArrayList<Character>();
        characters.add('a');
        characters.add('x');
        characters.add('z');
        characters.add('q');


        QuickSort quickSort = new QuickSort();
        MergeSort mergeSort = new MergeSort();
        InsertionSort insertionSort = new InsertionSort();
        SelectionSort selectionSort = new SelectionSort();

        System.out.println(insertionSort.sortIntegers(list_integers).toString());
        System.out.println(mergeSort.sortDoubles(list_doubles).toString());
        System.out.println(quickSort.sortStrings(list_strings).toString());
        System.out.println(selectionSort.sortCharacters(characters).toString());

        CompareSortingAlgorithms algorithmsComparator = new CompareSortingAlgorithms();

        System.out.println(algorithmsComparator.compare(list_integers, Integer::compareTo));
        System.out.println(algorithmsComparator.compare(list_doubles, Double::compareTo));
        System.out.println(algorithmsComparator.compare(list_strings, String::compareTo));
        System.out.println(algorithmsComparator.compare(characters, Character::compareTo));

    }
}
