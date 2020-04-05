public class TimeComparison<T> {

    public long compareSorts(SortingAlgorithm alg, T arr[]){

        long startTime = System.currentTimeMillis();

        alg.sort(arr);

        long elapsedTime = System.currentTimeMillis()-startTime;
        return elapsedTime;
    }
    
}
