package sorting;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class SelectionSortTest {
    private List<Integer> toTest = new ArrayList<>();
    private SortingAlgorithm<Integer> sortingAlgorithm = new SelectionSort<>();
    private Random random = new Random();

    @BeforeEach
    void generateList() {
        int listSize = 1000;
        for (int i = 0; i < listSize; i++) {
            toTest.add(random.nextInt());
        }
    }

    @Test
    void selectionSortTest() {
        List<Integer> expected = new ArrayList<>(List.copyOf(toTest));
        expected.sort(Integer::compareTo);
        toTest = sortingAlgorithm.sort(toTest);
        assertEquals(expected, toTest);
    }

}