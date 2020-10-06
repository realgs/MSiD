#include "Sorting.h"



Sorting::Sorting()
{
}


Sorting::~Sorting()
{

}

double * Sorting::selectionSort(double * arr, int length)
{
	if (length <= 0) 
	{
		return nullptr;
	}
	int min;
	for (int i = 0; i < length - 1; i++)
	{
		min = i;
		for (int j = i + 1; j < length; j++)
		{
			if (arr[j] < arr[min])
			{
				min = j;
			}
		}
		if (min != i)
		{
			double help = arr[i];
			arr[i] = arr[min];
			arr[min] = help;
		}
	}
	return arr;
}

double * Sorting::bubbleSort(double * arr, int length)
{
	int last_index = length - 1;
	for (int i = 0; i <= last_index; i++)
	{
		for (int j = 1; j <= last_index; j++)
		{
			if (arr[j] < arr[j - 1]) 
			{
				double help = arr[j];
				arr[j] = arr[j - 1];
				arr[j - 1] = help;
			}
		}
		last_index--;
	}
	return arr;
}




