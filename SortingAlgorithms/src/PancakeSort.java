class PancakeSort implements SortingAlgorithm{

  double[] sortedList;
  int size;

  @Override
  public double[] sort(double[] list, int size) {
    this.size = size;
    sortedList = new double[size];
    System.arraycopy(list, 0, sortedList, 0, size);
    pancakeSort();
    return sortedList;
  }

  private void pancakeSort() {
    for (int currSize = size-1; currSize > 1; currSize--) {

      int mi, i;
      for (mi = 0, i = 1; i < size; i++) {
        if (sortedList[i] > sortedList[mi]) mi = i;
      }

      if (mi != currSize) {
        flip(i);
        flip(currSize);
      }
    }
  }

  private void flip(int i) {
    double temp;
    int start = 0;
    while (start < i)
    {
      temp = sortedList[start];
      sortedList[start] = sortedList[i];
      sortedList[i] = temp;
      start++;
      i--;
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
