public class BubbleSort {
    double[] bubbleSort(double[] table){
        int rightMaxIndex = table.length - 1;
        while(rightMaxIndex > 0){
            int lastChecked = 0;
            for(int i=0; i<rightMaxIndex; i++){
                if(table[i] > table[i+1]){
                    swap(table, i, i+1);
                    lastChecked = i;
                }
            }
            rightMaxIndex = lastChecked;
        }
        return table;
    }

    void swap(double[] table, int index1, int index2){
        double temp = table[index2];
        table[index2] = table[index1];
        table[index1] = temp;
    }
}