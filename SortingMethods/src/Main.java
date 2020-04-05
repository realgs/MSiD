import java.util.Arrays;
import java.util.Random;

public class Main {


    static void randArrayInt(Integer arr[]) {
        Random rand = new Random();
        for (int i = 0; i < 100000; i++) {
            arr[i] = rand.nextInt();
        }

    }

    static void randArrayDouble(Double arr[]){
        Random rand = new Random();
            for(int i=0;i<100000;i++){
                arr[i]=rand.nextDouble();
            }

        }



    public static void main(String[] args) {

    Double arr[]= new Double[100000];
    randArrayDouble(arr);
    Integer arr1[]=new Integer[100000];
    randArrayInt(arr1);
    String arr3[]={"ala","kuba","ania","adam","patryk"};
    Integer arr2[]=Arrays.copyOf(arr1,arr1.length);
    Double arr4[]= Arrays.copyOf(arr,arr.length);
    Double arr5[]= Arrays.copyOf(arr,arr.length);

    TimeComparison<Integer> quickTime = new TimeComparison();
    TimeComparison<Double> quickTime2 = new TimeComparison();
    TimeComparison<String> quickTime3 = new TimeComparison();

    SortingAlgorithm<Integer> quickSort= new QuickSort();
    long time1=quickTime.compareSorts(quickSort,arr1);
    SortingAlgorithm<Double> quickSortd= new QuickSort();
    long time = quickTime2.compareSorts(quickSortd,arr);
    SortingAlgorithm<String> quickSorts= new QuickSort();
    long time3 = quickTime3.compareSorts(quickSorts,arr3);
    SortingAlgorithm<Integer> mergeSort= new MergeSort();
    long time2 = quickTime.compareSorts(mergeSort,arr2);
    SortingAlgorithm<Double> bitonicSort = new BitonicSort();
    long time4 = quickTime2.compareSorts(bitonicSort,arr4);
    SortingAlgorithm<Double> shellSort = new ShellSort();
    long time5 = quickTime2.compareSorts(shellSort,arr5);

    /*System.out.println(Arrays.toString(arr));
    System.out.println(time);
    System.out.println(Arrays.toString(arr1));
    System.out.println(time1);
    System.out.println(Arrays.toString(arr3));
    System.out.println(time3);
    System.out.println(Arrays.toString(arr2));
    System.out.println(time2);
    System.out.println(Arrays.toString(arr4));
    System.out.println(time4);
    System.out.println(Arrays.toString(arr5));
    System.out.println(time5);*/

    System.out.println("Time of quick, bitonic and shell sort");
        System.out.println(time);
        System.out.println(time4);
        System.out.println(time5);

    }
}
