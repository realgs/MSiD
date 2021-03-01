#include "BubbleSort.h"
#include "Generator.h"
#include <iostream>
#include <chrono>
using namespace std;
BubbleSort::BubbleSort(int ammount, int volume) {
	this->length = ammount;
	tab = new int[length];
	Generator g( volume);
	g.vGenerate(tab, length);

}
BubbleSort::~BubbleSort() {
	delete[] tab;
}
void BubbleSort::vShow() {
	for (int i = 0; i < length;i++) {
		cout << tab[i] << endl;
	}
}
void BubbleSort::vSwap(int i, int j) {
	
		int obj = tab[i];
		tab[i] = tab[j];
		tab[j] = obj;
	
}
void BubbleSort::vSort() {
	auto start = chrono::high_resolution_clock::now();
	for (int i = 0; i < length; i++) {
		for (int j = 0; j < length - 1; j++) {
			if (tab[j ] > tab[j+1]) {
				vSwap(j, j + 1);
			}
		}
	}
	auto stop = chrono::high_resolution_clock::now();
	chrono::duration<double> elapsed = stop - start;
	cout << "It takes for BubbleSort" << elapsed.count() << endl;
}