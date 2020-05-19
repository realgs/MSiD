#pragma once
#include <iostream>
#include <ctime>
#include <string>
using namespace std;
class Sorting
{
public:
	Sorting();
	~Sorting();

	double* selectionSort(double* arr, int length);
	double* bubbleSort(double* arr, int length);
	double* insertionSort(double* arr, int length);
	double* gnomeSort(double* arr, int length);

	unsigned int workingTime(int algorithm_num, double * arr, int length);
};

