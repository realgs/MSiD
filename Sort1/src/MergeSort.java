
public class MergeSort {
    public void sort (int [] tab,int indB,int indE) {
    if (indB<indE) {
        int indM = (indB + indE) / 2;
        sort(tab, indB, indM);
        sort(tab, (indM+1), indE);
        merge(tab, indB, indM, indE);
       
    }
    }
    private void merge (int [] tab, int indB,int indM,int indE) {
        int sizel=indM-indB+1;
        int sizer=indE-indM;
        int [] tabL=new int [sizel];
        int [] tabR=new int [sizer];

        for (int i=0;i<sizel;i++) {
            tabL[i]=tab[i+indB];
        }
        for (int i=0;i<sizer;i++) {
            tabR[i]=tab[i+indM+1];
        }
        int indHleft=0;
        int indHright=0;
        int generalIndex=indB;
        while ((indHleft<sizel)&&(indHright<sizer)) {

        if (tabL[indHleft]<tabR[indHright]){
            tab[generalIndex]=tabL[indHleft];
            generalIndex++;
            indHleft++;
        }
        else {
            tab[generalIndex]=tabR[indHright];
            generalIndex++;
            indHright++;
        }
        }
        while (indHright<sizer){
            tab[generalIndex]=tabR[indHright];
            generalIndex++;
            indHright++;
        }
        while (indHleft<sizel){
            tab[generalIndex]=tabL[indHleft];
            generalIndex++;
            indHleft++;
        }


    }

}
