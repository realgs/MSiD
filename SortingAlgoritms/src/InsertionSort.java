


import java.util.Comparator;
import java.util.List;


public class InsertionSort extends Sort{

    public <T> List<T> sort(List<T> list, Comparator<? super T> comparator) {

        for(int i=0; i<list.size(); i++)
        {
            for( int j=i; j>0; j--)
            {
                if(less(list.get(j), list.get(j-1),comparator))
                {
                    exchange(list,j,j-1);

                }
            }
        }

        return list;
    }
}