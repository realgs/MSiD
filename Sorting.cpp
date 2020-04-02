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

double * Sorting::insertionSort(double * arr, int length)
{
	double key = 0;
	int i = 0;
	for (int j = 1; j < length; j++) {
		key = arr[j];
		i = j - 1;
		while (i >= 0 && arr[i] > key) {
			arr[i + 1] = arr[i];
			i = i - 1;
			arr[i + 1] = key;
		}
	}
	return arr;
}

double * Sorting::gnomeSort(double * arr, int length)
{
	double temp;
	int i = 0;
	while (i < length) {
		if (i == 0 || arr[i - 1] <= arr[i])
			i++;
		else {
			temp = arr[i - 1];
			arr[i - 1] = arr[i];
			arr[i] = temp;
			i = i - 1;
		}
	}
	return arr;
}

unsigned int Sorting::workingTime(int algorithm_num, double * arr, int length)
{
	if (algorithm_num == 0)
	{ 
		unsigned int start_time = clock();
		this->selectionSort(arr, length);
		unsigned int end_time = clock();
		unsigned int search_time = end_time - start_time;
		return search_time;
	} 
	else if (algorithm_num == 1)
	{
		unsigned int start_time = clock();
		this->bubbleSort(arr, length);
		unsigned int end_time = clock();
		unsigned int search_time = end_time - start_time;
		return search_time;
	}
	else if (algorithm_num == 2)
	{
		unsigned int start_time = clock();
		this->insertionSort(arr, length);
		unsigned int end_time = clock();
		unsigned int search_time = end_time - start_time;
		return search_time;
	}
	else 
	{
		unsigned int start_time = clock();
		this->gnomeSort(arr, length);
		unsigned int end_time = clock();
		unsigned int search_time = end_time - start_time;
		return search_time;
	}
	
	
}







