import java.util.Random;

public class Comparison {
    public static void main(String[] args) {
        int cap = 100;
    int table[] = new int[cap];
        Random r=new Random(1000);
        for (int i = 0; i < table.length; i++) {
            table[i] = r.nextInt();
        }
        int tableBubble[] = new int[cap];
        int tableMerge[] = new int[cap];
        int tableHeap[] = new int[cap];
        int tableInsert[] = new int[cap];
        System.arraycopy(table, 0, tableBubble,0, cap);
        System.arraycopy(table, 0, tableMerge,0, cap);
        System.arraycopy(table, 0, tableHeap,0, cap);
        System.arraycopy(table, 0, tableInsert,0, cap);
        long start, stop, time;
        start = System.nanoTime();
        BubbleSort.sort(tableBubble);
        stop = System.nanoTime();
        System.out.println("BubbleSort = " + (stop-start));
        start = System.nanoTime();
        HeapSort.sort(tableHeap);
        stop = System.nanoTime();
        System.out.println("HeapSort = " + (stop-start));
        start = System.nanoTime();
        MergeSort.sort(tableMerge, 0, cap-1);
        stop = System.nanoTime();
        System.out.println("MergeSort = " + (stop-start));
        start = System.nanoTime();
        InsertSort.sort(tableInsert);
        stop = System.nanoTime();
        System.out.println("InsertSort = " + (stop-start));


    }
}
