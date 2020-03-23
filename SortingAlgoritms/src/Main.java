import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    public static void main(String args[]){
        List<Integer> list_integers = new ArrayList<>();
        Integer[] tab = {123, 12, 122, 34, 34, -12, 4, 127, 42, 8, 3};
        Collections.addAll(list_integers,tab);

        List<Double> list_doubles = new ArrayList<>();
        Double[] tab2 = {1.0,3.5, 12.1, 3.4,1.1,32.1};
        Collections.addAll(list_doubles,tab2);

        List<String> list_strings = new ArrayList<>();
        String[] strings = {"kot","pies","zając", "krowa", "biedronka", "moj_brat_michal"};
        Collections.addAll(list_strings, strings);


        List<Character> characters = new ArrayList<Character>();
        characters.add('a');
        characters.add('x');
        characters.add('z');
        characters.add('q');


        System.out.println(MergeSort.sortIntegers(list_integers).toString());
        System.out.println(QuickSort.sortDoubles(list_doubles).toString());
        System.out.println(MergeSort.sortStrings(list_strings).toString());
        System.out.println(QuickSort.sortCharacters(characters).toString());



    }
}
