public class MergeSort {

    static void sort(int tab[], int first, int last){


        if(first<last){
            int middle=(first+last)/2;
            sort(tab, first, middle);
            sort(tab, middle+1,last);
            merge(tab,first,middle,last);
        }
    }
    static void merge(int tab[], int first, int middle, int last){
        int leftHalf = middle - first + 1;
        int rightHalf = last - middle;
        int left[] = new int [leftHalf];
        int right[] = new int [rightHalf];
        for (int i=0; i<leftHalf; ++i)
            left[i] = tab[first + i];
        for (int j=0; j<rightHalf; ++j)
            right[j] = tab[middle + 1+ j];

        int i = 0, j = 0;
        int a = first;
        while (i < leftHalf && j < rightHalf){
            if (left[i] <= right[j]){
                tab[a] = left[i];
                i++;
            }
            else{
                tab[a] = right[j];
                j++;
            }
            a++;
        }
        while (i < leftHalf){
            tab[a] = left[i];
            i++;
            a++;
        }
        while (j < rightHalf)
        {
            tab[a] = right[j];
            j++;
            a++;
        }
    }
}