

public class SortingAlgorithms {


 public static void bubbleSort(int[] array) {

     int temp;

     for (int i = array.length - 1; i > 0; i--) {
         for (int j = 0; j < i; j++) {
             if (array[j] > array[j+1]) {
                 temp = array[j];
                 array[j] = array[j+1];
                 array[j+1] = temp;
             }
         }
     }


 }

 public static void printArrayOriginalBeforeBubbleSort(int[] array) {
     System.out.print("The original array: " );
     for (int i = 0; i < array.length; i++) {
         System.out.print(array[i] + ", ");
     }
     System.out.println();
 }

 public static void printArrayBubbleSorted(int[] array) {
     System.out.print("The sorted array: " );
     for (int i = 0; i < array.length; i++) {
         System.out.print(array[i] + ", ");
     }
     System.out.println();
 }


 public static void main(String[] args) {
     int[] array = {3, 92, 406, 1, 7, 3, 21, 2, 832, 14291, 454012, 12};
     System.out.println();
     printArrayOriginalBeforeBubbleSort(array);
     bubbleSort(array);
     printArrayBubbleSorted(array);
 }


}
