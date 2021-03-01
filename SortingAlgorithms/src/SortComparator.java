import java.util.ArrayList;

public class SortComparator {

  private ArrayList<Long> results;

  public ArrayList<Long> compareAlgorithms(ArrayList<SortingAlgorithm> algorithmList, double[] list, int size){
    results = new ArrayList<Long>();
    for(int i = 0; i < algorithmList.size(); i++){
      long start = System.nanoTime();
      algorithmList.get(i).sort(list, size);
      results.add(System.nanoTime() - start);
    }
    return results;
  }

  public void printResults(){
    for(int i = 0; i < results.size(); i++){
      System.out.println("Result of algorithm " + i + ": " + results.get(i));
    }
  }

}
