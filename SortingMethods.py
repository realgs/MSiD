import Measurement
import random


class SortingMethods:

    @staticmethod
    def swap(list, index1, index2):
        list[index1], list[index2] = list[index2], list[index1]

    def bubble_sort(self, sortable_list):
        n = len(sortable_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sortable_list[j] > sortable_list[j + 1]:
                    self.swap(sortable_list, j, j + 1)

    def partition(self, array, low, high):
        pivot = array[high]
        i = low
        for j in range(low, high):
            if array[j] < pivot:
                self.swap(array, i, j)
                i = i + 1
        self.swap(array, i, high)
        return i

    def quick_sort_ranged(self, array, low, high):
        if low < high:
            p = self.partition(array, low, high)
            self.quick_sort_ranged(array, low, p - 1)
            self.quick_sort_ranged(array, p + 1, high)

    def quick_sort(self, array):
        self.quick_sort_ranged(array, 0, len(array) - 1)

    def insert_sort(self, array):
        i = 1
        while i < len(array):
            x = array[i]
            j = i - 1
            while j >= 0 and array[j] > x:
                array[j + 1] = array[j]
                j = j - 1
            array[j + 1] = x
            i += 1

    # Marcin Ciura's gap sequence
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    def shell_sort(self, array):
        for gap in self.gaps:
            for i in range(gap, len(array)):
                tmp = array[i]
                j = i
                while j >= gap and array[j - gap] > tmp:
                    array[j] = array[j - gap]
                    j = j - gap
                array[j] = tmp


# tests:


arr = [random.uniform(1, 10000) for _ in range(10000)]

arr1 = arr.copy()
arr2 = arr.copy()
arr3 = arr.copy()
sm = SortingMethods()
print("Bubblesort: " + str(Measurement.measure_time(lambda: sm.bubble_sort(arr))))
print("Insertsort: " + str(Measurement.measure_time(lambda: sm.insert_sort(arr1))))
print("Shellsort: " + str(Measurement.measure_time(lambda: sm.shell_sort(arr2))))
print("Quicksort: " + str(Measurement.measure_time(lambda: sm.quick_sort(arr3))))
