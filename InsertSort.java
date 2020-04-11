public class InsertSort {


    void sort(int[] tab){
        for (int i = 1; i < tab.length; ++i) {
            int key = tab[i], j = i - 1;

            while (j >= 0 && tab[j] > key) {
                tab[j + 1] = tab[j];
                j--;
            }

            tab[j + 1] = key;
        }


    }
}