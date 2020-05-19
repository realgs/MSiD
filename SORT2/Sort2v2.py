import time
import random


class Sort2:

    def __init__(self,amount,volume):
        self.amount=amount
        self.volume=volume
        self.list=[]

    def show(self):
        for a in self.list:
            print(a)
    def generate(self):
        random.seed()
        for el in range (0,self.amount):
            a=random.randint(0,self.volume)
            self.list.append(a)

    def quickSort(self, left, right):
        if left<right:

            pi=self.partition(left,right)

            self.quickSort( left,pi-1)
            self.quickSort(pi+1,right)

    def partition(self, left, right):
        pivot=self.list[right]

        i=left-1
        for it in range (left,right):
            if self.list[it]<pivot:

                i=i+1
                self.list[i],self.list[it]=self.list[it],self.list[i]

        self.list[i+1],self.list[right]=self.list[right], self.list[i+1]
        return(i+1)


    def start(self):
        self.generate()
        t = time.process_time()
        self.quickSort(0,self.amount-1)
        b=time.process_time()-t
        print(b)


sort=Sort2(10000,10000)
sort.start()


