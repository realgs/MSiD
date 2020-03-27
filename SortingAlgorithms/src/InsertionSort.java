public class InsertionSort implements SortingAlgorithm {

  double[] sortedList;
  int size;

  @Override
  public double[] sort(double[] list, int size) {
    this.size = size;
    sortedList = new double[size];
    System.arraycopy(list, 0, sortedList, 0, size);
    insertionSort();
    return sortedList;
  }

  private void insertionSort(){
    for(int i = 1; i < size; i++) {
      for (int j = i; j > 0; j--) {
        if(sortedList[j-1] > sortedList[j]){
          swap(sortedList, j-1, j);
        }
        else j = 0;
      }
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
