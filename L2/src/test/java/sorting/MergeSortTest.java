package sorting;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

class MergeSortTest {
    private List<Integer> toTest = new ArrayList<>();
    private SortingAlgorithm<Integer> sortingAlgorithm = new MergeSort<>();
    private Random random = new Random();

    @BeforeEach
    void generateList() {
        int listSize = 1000;
        for (int i = 0; i < listSize; i++) {
            toTest.add(random.nextInt());
        }
    }

    @Test
    void mergeSortTest() {
        List<Integer> expected = new ArrayList<>(List.copyOf(toTest));
        expected.sort(Integer::compareTo);
        toTest = sortingAlgorithm.sort(toTest);
        assertEquals(expected, toTest);
    }

}