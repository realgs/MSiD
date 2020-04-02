#include <iostream>
#include "Sorting.h"
using namespace std;
void printArr(double *arr, int length)
{
	for (int i = 0; i < length; i++)
	{
		cout << arr[i] << endl;
	}
}
int main()
{
	{
		Sorting s;

		double* arr0 = new double[3];
		arr0[0] = 9;
		arr0[1] = 89;
		arr0[2] = 10.4;

		double* arr1 = new double[3];
		arr1[0] = 9;
		arr1[1] = 89;
		arr1[2] = 10.4;

		double* arr2 = new double[3];
		arr2[0] = 9;
		arr2[1] = 89;
		arr2[2] = 10.4;

		double* arr3 = new double[3];
		arr3[0] = 9;
		arr3[1] = 89;
		arr3[2] = 10.4;

		unsigned int selectionSortRes = s.workingTime(0, arr0, 3);
		unsigned int bubbleSortRes = s.workingTime(1, arr1, 3);
		unsigned int insetrionSortRes = s.workingTime(2, arr2, 3);
		unsigned int gnomeSortRes = s.workingTime(3, arr3, 3);

		cout <<"selection sort:  "<< selectionSortRes << endl;
		cout <<"bubble sort: " <<bubbleSortRes << endl;
		cout << "insertion sort: "<<insetrionSortRes << endl;
		cout << "gnome sort: "<<gnomeSortRes << endl;
	}
	system("pause");
	return 0;
}