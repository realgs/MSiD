public class Main {

    public static void main(String[] args) {
int [] tab={1,6,2,5,3,4};
MergeSort test=new MergeSort();
test.sort(tab,0,5);
for (int i=0;i<6;i++){
    System.out.println(tab[i]);
}
    }
}
