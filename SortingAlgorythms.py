def replace(arr,i,j):
	elem = arr[i]
	arr[i] = arr[j]
	arr[j] = elem

def bubbleSort(arr):

	n = 0

	for i in range(len(arr)):
		
		for j in range(n,len(arr)-1):

			if arr[j+1] < arr[j]: 			
				replace(arr,j+1,j)	
		n = n+1

def selectSort(arr):
	
	for i in range(0,len(arr)-1):
		indexOfMin = i
		minElem = arr[i]
		for j in range(i+1,len(arr)-1):
			if arr[j] < minElem:
				minElem = arr[j]
				indexOfMin = j		
		replace(arr,i,indexOfMin)

arr = [1,7,2,4,10,13]

for i in arr:
	print(i)

print('\n')

selectSort(arr)

for i in arr:
	print(i)

print('\n')

bubbleSort(arr)

for i in arr:
	print(i)
