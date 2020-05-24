#include "InsertSort.h"
#include "BubbleSort.h"
#include <iostream>
using namespace std;
int main()
{
    InsertSort sort1(10000, 100000);
    sort1.vSort();
   
    BubbleSort sort2(10000, 100000);
    sort2.vSort();
  
    return 0; 
}

