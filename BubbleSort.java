public class BubbleSort {

    static void switchPlaces(int[] tab, int index1, int index2){
        int temp = tab[index1];
        tab[index1] = tab[index2];
        tab[index2] = temp;
    }
    static void sort(int[] tab){
        for(int j=0; j<tab.length-1;j++){
            for (int i=0; i<tab.length-1-j; i++){
                if (tab[i]>tab[i+1]){
                  switchPlaces(tab,i, i+1);
                }
             }
            //changed
        }
    }
}
