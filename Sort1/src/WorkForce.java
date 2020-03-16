public class WorkForce extends Thread {
 private int indB;
 private int indE;
 private int [] tab;

    public WorkForce(int indB,int indE,int [] tab){
        this.indB=indB;
        this.indE=indE;
        this.tab=tab;
    }

}
