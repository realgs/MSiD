import kotlinx.coroutines.*

object StockOperations{

  fun getPercantageDiff(buySell: BuySell) : Double{
    return 1 - (buySell.sell - buySell.buy) / buySell.buy
  }

  suspend fun watchStock(methodToExecute : () -> BuySell): BuySell {
      return methodToExecute()
  }

  suspend fun watchAllStocks(methodsToExecute: List<() -> BuySell>): List<BuySell> {

    val deferred = methodsToExecute.map { stock ->
      GlobalScope.async {
        stock()
      }
    }

    return deferred.map { it.await() }

  }

}


