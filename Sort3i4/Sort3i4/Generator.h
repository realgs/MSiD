#pragma once
class Generator {
public:
	Generator(int max);
	void vGenerate(int* tab,int length);
private:
	int max;
};