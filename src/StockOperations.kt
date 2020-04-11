import kotlinx.coroutines.*

object StockOperations{

  private fun getPercantageDiff(buySell: BuySell) : Double{
    return 1 - (buySell.sell - buySell.buy) / buySell.buy
  }

  suspend fun watchStock(refreshFreq: Long = 5000, methodToExecute : () -> BuySell) {
    while(true){
      val response : BuySell = methodToExecute()
      println(response)
      println(StockOperations.getPercantageDiff(response))
      delay(refreshFreq)
    }
  }

}


