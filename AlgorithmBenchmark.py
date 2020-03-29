import SortingMethods
import Measurement

Sorts = [SortingMethods.bubble_sort,
         SortingMethods.insert_sort,
         SortingMethods.shell_sort,
         SortingMethods.quick_sort]

Measurement.benchmark_sorting_functions(Sorts)