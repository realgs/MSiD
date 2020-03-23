import array

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
			
arr = [1,7,2,4,10,13]

for i in arr:
	print(i)

print('\n')

bubbleSort(arr)

for i in arr:
	print(i)
