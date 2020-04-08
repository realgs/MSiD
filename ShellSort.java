import java.util.ArrayList;

public class ShellSort<T extends Comparable<? super T>> implements ArrayListSorter<T> {
    @Override
    public void sort(ArrayList<T> list) {
        ArrayList<Integer> gapSequences = createGapSequences();

        int iteration = 1;
        int dist = gapSequences.get(gapSequences.size() - iteration);

        while (dist > 0){
            for (int i = dist ; i < list.size() ; ++i) {
                T element = list.get(i);
                int j;
                for (j = i ; j >= dist && element.compareTo(list.get(j - dist)) < 0 ; j -= dist) {
                    list.set(j, list.get(j - dist));
                }

                list.set(j, element);
            }
            dist = gapSequences.get(gapSequences.size() - ++iteration);
        }
    }

    private ArrayList<Integer> createGapSequences(){
        int gapSequencesAmount = 70;

        ArrayList<Integer> distances = new ArrayList<>(gapSequencesAmount + 1);
        distances.add(0);
        double distance;

        for(int i = 0 ; i < gapSequencesAmount ; i++){
            distance = 1.8 * Math.pow(2.25, i) - 0.8;
            distances.add((int) (Math.ceil(distance)));
        }

        return distances;
    }
}
