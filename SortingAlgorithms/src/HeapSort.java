import java.util.ArrayList;
import java.util.List;

public class HeapSort implements SortingAlgorithm{

  double[] sortedList;
  int size;

  @Override
  public double[] sort(double[] list, int size) {

      this.size = size;
      sortedList = new double[size];
      sortedList = list;
      heapsort(sortedList, size);
      return sortedList;

    }

    private void heapsort(double[] heap, int n) {
      heapAdjustment(heap, n);

      for(int i = n-1; i > 0; i--){
        swap(heap,i,0);
        heapify(heap,0, i);
      }
    }

    private void swap(double[] list, int left, int right) {
      if (left != right) {
        double temp = list[left];
        list[left] = list[right];
        list[right] = temp;
      }
    }


    public void heapify(double[] heap,int idx, int n){
      int idxOfBigger=2*idx+1;
      if(idxOfBigger<n){
        if(idxOfBigger+1<n && heap[idxOfBigger] < heap[idxOfBigger+1]) idxOfBigger++;
        if(heap[idx] < heap[idxOfBigger]){
          swap(heap,idx,idxOfBigger);
          heapify(heap,idxOfBigger,n);
        }
      }
    }


    void heapAdjustment(double[] heap,int n) {
      for(int i=(n-1)/2; i>=0; i--)
        heapify(heap, i, n);
    }

    public String toString() {
      String wynik = "";
      for(int i = 0; i < size; i++) {
        wynik += sortedList[i] + "\n";
      }
      return wynik;
    }
  }

