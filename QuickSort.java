import java.util.ArrayList;
import java.util.List;

public class QuickSort<T extends Comparable<? super T>> {
    
    int partition(List<T> list, int startIndex, int endIndex)
    {
        T pivot = list.get(endIndex);
        int i = (startIndex-1);
        for (int j=startIndex; j<endIndex; j++)
        {
            if (list.get(j).compareTo(pivot) < 0 )
            {
                i++;
                T swapHelp = list.get(i);
                list.set(i,list.get(j));
                list.set(j, swapHelp);
            }
        }
        T swapHelp = list.get(i+1);
        list.set(i+1, list.get(endIndex));
        list.set(endIndex, swapHelp);

        return i+1;
    }


    void sort(List<T> list, int startIndex, int endIndex)
    {
        if (startIndex < endIndex)
        {
            int pi = partition(list, startIndex, endIndex);

            sort(list, startIndex, pi-1);
            sort(list, pi+1, endIndex);
        }
    }

