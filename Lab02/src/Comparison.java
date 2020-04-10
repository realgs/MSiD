import java.util.ArrayList;

public class Comparison<T> {

    public long executionTime(ArrayListSorting<T> alg, ArrayList<T> list) {
        ArrayList<T> tmp = new ArrayList<>(list);
        long start = System.currentTimeMillis();
        alg.sort(tmp);
        return System.currentTimeMillis() - start;
    }
}
