import java.util.Comparator;
import java.util.List;

public abstract class Sort {

    protected static <T> boolean less(T o1, T o2, Comparator<? super T> comparator) {
        return comparator.compare(o1,o2)<0;

    }

    protected static <T> void exchange(List<T> list, int o1Pos, int o2Pos) {

        T temp = list.get(o1Pos);
        list.set(o1Pos,list.get(o2Pos));
        list.set(o2Pos,temp);
    }

    protected static <T> void exchange(List<T> list, Object o1, Object o2) {
        exchange(list,list.indexOf(o1),list.indexOf(o2));
    }

    protected abstract  <T> List<T> sort(List<T> list, Comparator<? super T> comparator);

    public  List<String> sortStrings(List<String> list){
        return sort(list, String::compareTo);

    }

    public  List<Character> sortCharacters(List<Character> list){
        return sort(list, Character::compareTo);

    }

    public  List<Double> sortDoubles(List<Double> list){
        return sort(list, Double::compareTo);

    }

    public  List<Integer> sortIntegers(List<Integer> list){
        return sort(list, Integer::compareTo);

    }
}
