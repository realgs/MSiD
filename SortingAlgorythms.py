import time
from random import seed
from random import randint

def replace(arr,i,j):
	elem = arr[i]
	arr[i] = arr[j]
	arr[j] = elem

def bubbleSort(arr):

	for i in range(len(arr)):

		for j in range(len(arr)-1-i):

			if arr[j+1] < arr[j]:
				replace(arr,j+1,j)


def selectSort(arr):

	for i in range(0,len(arr)):
		indexOfMin = i
		minElem = arr[i]
		for j in range(i+1,len(arr)):
			if arr[j] < minElem:
				minElem = arr[j]
				indexOfMin = j
		replace(arr,i,indexOfMin)


def quickSortPrivate(arr,i,j):
	if i >= j:
		return
	pivotIndex = (int)((j+i)/2)
	replace(arr,j,pivotIndex)
	pivotIndex = j
	r = j
	l = i
	while r!=l:
		while arr[l] <= arr[pivotIndex] and r!=l:
			l = l + 1
		if r != l:
			replace(arr,l,pivotIndex)
			pivotIndex = l
			r = r - 1
		while arr[r] >= arr[pivotIndex] and r!=l:
			r = r - 1
		if r != l:
			replace(arr,r,pivotIndex)
			pivotIndex = r
			l = l + 1
	quickSortPrivate(arr,i,pivotIndex-1)
	quickSortPrivate(arr,pivotIndex+1,j)

def quickSort(arr):
	quickSortPrivate(arr,0,len(arr)-1)

def insertSort(arr):
	for i in range(len(arr)):
		j = 0
		bool = False
		while j<i and (not bool):
			if arr[j] > arr[i]:
				bool = True
				arr.insert(j,arr[i])
				del arr[i+1]
			j = j + 1

def testSortingAlgorythm(arr,function):
	start = time.time()
	function(arr)
	end = time.time()
	print(end-start)

def randomIntegerArray(size):
	seed(1)
	arr = []
	for _ in range(size):
		arr.append(randint(0,100))
	return arr


arr = [1,7,2,4,10,13,3]

arr2 = arr.copy()

for i in arr:
	print(i)

print('\n')

insertSort(arr)

for i in arr:
	print(i)

print('\n')

arrSorted = arr.copy()
arr = arr2.copy()

bubbleSort(arr)

def checkIfSortedCorrectly(arr,arrSorted):
	for i in range(len(arr)):
		if arr[i] != arrSorted[i]:
			print("Something went wrong")
	arr = arr2.copy()

checkIfSortedCorrectly(arr,arrSorted)

selectSort(arr)

checkIfSortedCorrectly(arr,arrSorted)

quickSort(arr)

checkIfSortedCorrectly(arr,arrSorted)

for i in arr:
	print(i)



arr = randomIntegerArray(10000)

arr2 = arr.copy()

print("Bubblesort")
testSortingAlgorythm(arr,bubbleSort)

arr = arr2.copy()

print("Quicksort")
testSortingAlgorythm(arr,quickSort)

arr = arr2.copy()

print("Insertsort")
testSortingAlgorythm(arr,insertSort)

arr = arr2.copy()

print("Selectsort")
testSortingAlgorythm(arr,selectSort)
