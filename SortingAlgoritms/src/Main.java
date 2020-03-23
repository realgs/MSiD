import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String args[]){
        List<Integer> list = new ArrayList<>();
        Integer[] tab = {123, 12, 122, 34, 34, -12, 4, 127, 42, 8, 3};
        for (int i = 0; i < tab.length; i++) {
            list.add(tab[i]);

        }
        QuickSort.sort(list, Integer::compareTo);
        System.out.println(list.toString());

        List<Double> list1 = new ArrayList<>();
        Double[] tab2 = {1.0,3.5, 12.1, 3.4,1.1,32.1};
        for (int i = 0; i < tab2.length; i++) {
            list1.add(tab2[i]);

        }
        QuickSort.sort(list1, Double::compareTo);
        System.out.println(list1.toString());

        List<Character> characters = new ArrayList<Character>();
        characters.add('a');
        characters.add('x');
        characters.add('z');
       characters.add('q');

        QuickSort.sort(characters, Character::compareTo);
        System.out.println(characters.toString());



    }
}
