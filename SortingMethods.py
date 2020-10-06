
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

    def partition(self, array, start_index, end_index):
        pivot = array[end_index]
        i = start_index
        for j in range(start_index, end_index):
            if array[j] < pivot:
                self.swap(array, i, j)
                i = i + 1
        self.swap(array, i, end_index)
        return i

    def quick_sort_ranged(self, array, start_index, end_index):
        if start_index < end_index:
            p = self.partition(array, start_index, end_index)
            self.quick_sort_ranged(array, start_index, p - 1)
            self.quick_sort_ranged(array, p + 1, end_index)

    def quick_sort(self, array):
        self.quick_sort_ranged(array, 0, len(array)-1)


arr = [1, 999.99, 420.69, -22, -1.1]
sm = SortingMethods()
sm.quick_sort(arr)
print(arr)
