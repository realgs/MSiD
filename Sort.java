import java.util.List;

public interface Sort <T extends Comparable<? super T>>{
     void sort(List<T> list);

}
