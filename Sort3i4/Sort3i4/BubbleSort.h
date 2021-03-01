#pragma once
class BubbleSort {
public:
	BubbleSort(int ammount,int volume);
	~BubbleSort();
	void vShow();
	void vSort();
private:
	void vSwap(int i,int j);
	int* tab;
	int length;
};