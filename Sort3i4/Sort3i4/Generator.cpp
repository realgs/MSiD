#include <random>
#include <iostream>
#include "Generator.h"
using namespace std;
Generator::Generator(int max) {
	this->max = max;
	
}
void Generator::vGenerate(int *tab,int length) {
	std::random_device r;
	std::default_random_engine e1(r());
	std::uniform_int_distribution<int> uniform_dist(0, max);
	for (int i = 0; i < length; i++) {
		tab[i] = uniform_dist(e1);
	}

}