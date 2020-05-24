#pragma once
class InsertSort {
public:
	 InsertSort(int ammount, int volume);
	 ~InsertSort();
	 void vSort();
	 void vShow();
private:
	int* tab;
	int length;
		
};
