

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
         System.out.print(array[i] + " ");
     }
     System.out.println();
 }

 public static void printArrayBubbleSorted(int[] array) {
     System.out.print("The sorted array: " );
     for (int i = 0; i < array.length; i++) {
         System.out.print(array[i] + " ");
     }
     System.out.println();
 }

 public static void InsertSort(int[] array2) {

     for (int i = 1; i < array2.length; ++i) {
         int key = array2[i];
         int j = i - 1;

         while (j >= 0 && array2[j] > key) {
             array2[j+1] = array2[j];
             j = j - 1;
         }
         array2[j+1] = key;
     }
 }

 public static void printArrayOriginalBeforeInsertSort(int[] array2) {
     System.out.print("The original array: ");
     for (int i = 0; i < array2.length; i++) {
         System.out.print(array2[i] + " ");
     }
     System.out.println();

 }

 public static void printArrayInsertSorted(int[] array2) {
     System.out.print("The sorted array: ");
     for (int i = 0; i < array2.length; i++) {
         System.out.print(array2[i] + " ");
     }
     System.out.println();
 }


 



 public static void main(String[] args) {
     int[] array = {3, 92, 406, 1, 7, 3, 21, 2, 832, 14291, 454012, 12};
     int[] array2 = {7, 91, 102, 4, 1, 6, 39, 10, 32, 491, 4012, 123};

     System.out.println();
     System.out.println("BubbleSort");
     System.out.println();
     printArrayOriginalBeforeBubbleSort(array);
     bubbleSort(array);
     printArrayBubbleSorted(array);

     System.out.println();
     System.out.println("InsertSort");
     System.out.println();
     printArrayOriginalBeforeInsertSort(array2);
     InsertSort(array2);
     printArrayInsertSorted(array2);
 }


}
