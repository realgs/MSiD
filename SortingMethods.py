
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
        self.quick_sort_ranged(array, 0, len(array)-1)


arr = [1, 999.99, 420.69, -22, -1.1]
sm = SortingMethods()
sm.quick_sort(arr)
for i in range(len(arr)):
    print("%.2f" % arr[i]),
