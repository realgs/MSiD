#include <iostream>
#include "InsertSort.h"
#include "Generator.h"
#include <chrono>
#include <string>
using namespace std;
InsertSort::InsertSort(int ammount, int volume) {
	this->length = ammount;
	tab = new int[length];
	Generator g (volume);
	g.vGenerate(tab, length);
}
InsertSort::~InsertSort() {
	delete[] tab;
}
void InsertSort::vShow() {
	for (int i = 0; i < length; i++) {
		cout << tab[i] << endl;
	}
}
void InsertSort::vSort() {
	auto start = chrono::high_resolution_clock::now();
	int ival;
	int iter;
	for (int i = 1; i < length; i++) {
		ival = tab[i];
		iter = i - 1;
		while (iter >= 0 && tab[iter] > ival) {
			tab[iter + 1] = tab[iter];
			iter--;
		}
		tab[iter + 1] = ival;
	}
	auto stop = std::chrono::high_resolution_clock::now();
	chrono::duration<double> elapsed = stop - start;
	cout << "It takes for InsertSort" << elapsed.count() << endl;

}
