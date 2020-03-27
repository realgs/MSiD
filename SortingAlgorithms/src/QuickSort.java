import java.util.Random;

public class QuickSort implements SortingAlgorithm {

  int size;
  Random rnd = new Random();
  double[] sortedList;

  @Override
  public double[] sort(double[] list, int size) {
    this.size = size;
    sortedList = new double[size];
    System.arraycopy(list, 0, sortedList, 0, size);
    quicksort(sortedList, 0, size-1);
    return sortedList;

  }

  public void quicksort(double[] list, int startIdx, int endIdx){

    if(endIdx > startIdx) {
      int random = rnd.nextInt(endIdx-startIdx) + startIdx;
      double pivot = list[random];
      swap(list, random, startIdx);
      int i = startIdx+1;

      for(int j = startIdx+1; j <= endIdx; j++){
        if(pivot > list[j]){
          swap(list, j, i);
          i++;
        }
      }

      swap(list, i-1, startIdx);

      quicksort(list, startIdx, i-2);
      quicksort(list, i, endIdx);
    }
  }

  private void swap(double[] list, int left, int right) {

    if (left != right) {
      double temp = list[left];
      list[left] = list[right];
      list[right] = temp;
    }
  }

  public String toString() {
    String wynik = "";
    for(int i = 0; i < size; i++) {
      wynik += sortedList[i] + "\n";
    }
    return wynik;
  }
}
