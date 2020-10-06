

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



    public static void printArray(int[] array) {
        System.out.print("The original array: " );
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i] + " ");
        }
        System.out.println();
    }


 public static void main(String[] args) {
     System.out.println();

     int[] array = new int[]{3, 92, 406, 1, 7, 3, 21, 2, 832, 14291, 454012, 12};
     printArray(array);
     System.out.print("Bubble-sorted array: ");
     bubbleSort(array);

     for (int value: array) {
         System.out.print(value + " ");
     }
     System.out.println();

     System.out.println();

     int[] array2 = new int[]{2, 4, 6, 32, 1, 90, 64, 223, 91283, 6, 8, 3, 6032};
     printArray(array2);
     System.out.print("Insert-sorted array: ");
     InsertSort(array2);

     for (int value: array2) {
         System.out.print(value + " ");

 }
     System.out.println();

    }


}
