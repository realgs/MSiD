package sorting;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

class HeapSortTest {
    private List<Integer> toTest = new ArrayList<>();
    private HeapSort<Integer> sortingAlgorithm = new HeapSort<>();
    private Random random = new Random();

    @BeforeEach
    void generateList() {
        int listSize = 1000;
        toTest.clear();
        for (int i = 0; i < listSize; i++) {
            toTest.add(random.nextInt());
        }
    }

    @Test
    void sortTest() {
        List<Integer> expected = new ArrayList<>(List.copyOf(toTest));
        expected.sort(Integer::compareTo);
        toTest = sortingAlgorithm.sort(toTest);
        assertEquals(expected, toTest);
    }

    @Test
    void buildHeapTest() {
        toTest = sortingAlgorithm.builtHeap(toTest);
        for (int i = 0; i <= (toTest.size() - 3) / 2; i++) {
            assertTrue(toTest.get(i).compareTo(toTest.get(sortingAlgorithm.getLeftChild(i))) >= 0);
            assertTrue(toTest.get(i).compareTo(toTest.get(sortingAlgorithm.getRightChild(i))) >= 0);
        }

    }
}