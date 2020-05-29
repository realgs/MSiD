import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.random.Random

class Simulator(dataset: List<ChartData>){

  private val highData: DoubleArray = dataset.map { it.high }.toDoubleArray()
  private val lowData: DoubleArray = dataset.map { it.low }.toDoubleArray()
  private val openData: DoubleArray = dataset.map { it.open }.toDoubleArray()
  private val closeData: DoubleArray = dataset.map { it.close }.toDoubleArray()

  private val highChangeData: DoubleArray = getChangeData(highData)
  private val lowChangeData: DoubleArray = getChangeData(lowData)
  private val openChangeData: DoubleArray = getChangeData(openData)
  private val closeChangeData: DoubleArray = getChangeData(closeData)


  fun simulate(beginDate: Long, interval: Int): MutableList<ChartData> {
    val dsHigh = DescriptiveStatistics(highData)
    val dsLow = DescriptiveStatistics(lowData)
    val dsOpen = DescriptiveStatistics(openData)
    val dsClose = DescriptiveStatistics(closeData)

    val dsHighChange = DescriptiveStatistics(highChangeData)
    val dsLowChange = DescriptiveStatistics(lowChangeData)
    val dsOpenChange = DescriptiveStatistics(openChangeData)
    val dsCloseChange = DescriptiveStatistics(closeChangeData)

    println("${dsHigh.mean} ... ${dsHigh.max} ... ${dsHigh.min}")
    println("${dsHighChange.mean} ... ${dsHighChange.max} ... ${dsHighChange.min} ... ${dsHighChange.standardDeviation}")


    val newValues: MutableList<ChartData> = mutableListOf()
    var date = beginDate

    val highLowDifference = getHighAndLowDifference(highData, lowData)

    val deviationDataHigh = getValuesOutsideStandardDeviation(highData, dsHigh)
    val deviationDataOpen = getValuesOutsideStandardDeviation(openData, dsOpen)
    val deviationDataClose = getValuesOutsideStandardDeviation(closeData, dsClose)



    val newClose = generateNewVal(closeData.last(), closeData.size, dsClose, dsCloseChange, deviationDataClose, mutableListOf())
    val newOpen = setNewOpens(closeData.last(), newClose)


    val newHigh = generateNewHigh(openData, closeData, newOpen, newClose)
    val newLow = generateNewLow(openData, closeData, newOpen, newClose)


    for( i in 0 until newHigh.size) {
      newValues.add(ChartData(date, newHigh[i], newLow[i], newOpen[i], newClose[i]))
      date += interval
    }

    return newValues

  }

  fun generateNewHigh(openData: DoubleArray, closeData: DoubleArray, newOpenData: MutableList<Double>, newCloseData: MutableList<Double>): MutableList<Double> {
    val dsHighData = getStatsOfHighVal(highData, openData, closeData)
    println("HIGH DATA: ${dsHighData.mean} ... ${dsHighData.standardDeviation}")
    val retVal = mutableListOf<Double>()
    for(i in openData.indices) {
      val larger = max(newOpenData[i], newCloseData[i])
      val d100roll = Random.nextInt(0, 100)
      retVal.add(larger + ((dsHighData.mean + dsHighData.standardDeviation) / 100) * d100roll)
    }
    return retVal
  }

  fun generateNewLow(openData: DoubleArray, closeData: DoubleArray, newOpenData: MutableList<Double>, newCloseData: MutableList<Double>): MutableList<Double> {
    val dsLowData = getStatsOfLowVal(lowData, openData, closeData)
    println("LOW DATA: ${dsLowData.mean} ... ${dsLowData.standardDeviation}")
    val retVal = mutableListOf<Double>()
    for(i in openData.indices) {
      val smaller = min(newOpenData[i], newCloseData[i])
      val d100roll = Random.nextInt(0, 100)
      retVal.add(smaller - ((dsLowData.mean + dsLowData.standardDeviation) / 100) * d100roll)
    }
    return retVal
  }


  fun setNewOpens(firstVal: Double, closeData: MutableList<Double>): MutableList<Double> {
    val retVal = mutableListOf<Double>()
    retVal.add(firstVal)
    for(close in closeData){
      retVal.add(close)
    }
    return retVal.dropLast(1).toMutableList()
  }

  fun generateNewVal(prevVal: Double, threshold: Int, ds: DescriptiveStatistics, dsc: DescriptiveStatistics, deviationData: Pair<DoubleArray, DoubleArray>, acc: MutableList<Double>): MutableList<Double> {
    val dsValuesAboveDev = deviationData.first
    val dsValuesBelowDev = deviationData.second
    val newVal = generateValue(ds, dsc, dsValuesAboveDev, dsValuesBelowDev, prevVal)
    acc.add(newVal)
    if(threshold > 0) generateNewVal(newVal, threshold-1, ds, dsc, deviationData, acc)
    return acc
  }


//  fun generateNewLow(previousHigh: Double, currentHigh: Double, nextHigh: Double?, differenceData: DoubleArray): Double {
//    val dsDifference = DescriptiveStatistics(differenceData)
//    var startVal = min(currentHigh, previousHigh)
//    if(nextHigh != null) startVal = min(startVal, nextHigh)
//    val abnormalValues = getValuesOutsideStandardDeviation(differenceData, dsDifference)
//
//    val d100roll = Random.nextDouble(0.0, 1.0)
//    if(d100roll >= 1.0 - abnormalValues.first.size / differenceData.size) {
//      val rolledVal = Random.nextDouble(dsDifference.mean + dsDifference.standardDeviation, dsDifference.max)
//      return min(startVal, currentHigh - rolledVal)
//    }
//    else if (d100roll <= abnormalValues.second.size / differenceData.size) {
//      val rolledVal = Random.nextDouble(dsDifference.mean + dsDifference.standardDeviation, dsDifference.max)
//      return min(startVal, currentHigh - rolledVal)
//    }
//    val rolledVal = Random.nextDouble(dsDifference.mean - dsDifference.standardDeviation, dsDifference.mean + dsDifference.standardDeviation)
//    return min(startVal, currentHigh - rolledVal)
//  }

//  fun generateLows(newHighData: List<Double>, previousHigh: Double, differenceData: DoubleArray): MutableList<Double> {
//    val retVal = mutableListOf<Double>()
//    var prevVal = previousHigh
//    for(i in 0..newHighData.size-2){
//      retVal.add(generateNewLow(prevVal, newHighData[i], newHighData[i+1], differenceData))
//      prevVal = newHighData[i]
//    }
//    retVal.add(generateNewLow(prevVal, newHighData.last(), null, differenceData))
//    return retVal
//  }

  fun generateValue(ds: DescriptiveStatistics, dsChange: DescriptiveStatistics, valsAboveDev: DoubleArray, valsBelowDev: DoubleArray, previousValue: Double): Double {
    var growChance = 50.0

    val dsValAboveStat = DescriptiveStatistics(valsAboveDev)
    val dsValBelowStat = DescriptiveStatistics(valsBelowDev)

    if(previousValue > ds.mean) {
      growChance = 100.0 - (previousValue - ds.mean) / (dsValAboveStat.mean + dsValAboveStat.standardDeviation - ds.mean) * 100
      println("100.0 - ${(previousValue - ds.mean)} / ${(dsValAboveStat.mean + dsValAboveStat.standardDeviation - ds.mean)} * 100")
    }
    else if (previousValue < ds.mean){
      growChance = (ds.mean - previousValue) / (ds.mean - dsValBelowStat.mean - dsValBelowStat.standardDeviation) * 100
    }

    val d100Roll = Random.nextInt(0, 100)

    println("${growChance} - $d100Roll = ${growChance - d100Roll}")

    if(growChance - d100Roll > 0){
      val newVal = previousValue + rollNewVal(dsChange, dsValAboveStat)
      return newVal
    }
    else if(growChance - d100Roll < 0){
      val newVal = previousValue - rollNewVal(dsChange, dsValBelowStat)
      return newVal
    }

    return previousValue
  }

  fun rollNewVal(dsc: DescriptiveStatistics, dsCh: DescriptiveStatistics): Double {
    val changeRoll = Random.nextInt(0, 100)
    val extraVal = Random.nextDouble(0.0, dsCh.mean - dsc.mean + dsc.standardDeviation)
    val change = ((dsc.mean + dsc.standardDeviation) / 100) * changeRoll
    println(change)
    return change
  }

  fun getValuesOutsideStandardDeviation(data: DoubleArray, ds: DescriptiveStatistics): Pair<DoubleArray, DoubleArray> {
    val above = mutableListOf<Double>()
    val below = mutableListOf<Double>()
    data.forEach {
      if(it > ds.mean + ds.standardDeviation){
        above.add(it)
      }
      else if(it < ds.mean - ds.standardDeviation){
        below.add(it)
      }
    }
    return Pair(above.toDoubleArray(), below.toDoubleArray())
  }

  fun getChangeData(data: DoubleArray): DoubleArray {
    val resVal = mutableListOf<Double>()
    for(i in 1 until data.size){
      resVal.add(abs(data[i]-data[i-1]))
    }
    return resVal.toDoubleArray()
  }

  fun getHighAndLowDifference(dataHigh: DoubleArray, dataLow: DoubleArray): DoubleArray {
    val resVal = mutableListOf<Double>()
    for(i in dataHigh.indices){
      resVal.add(dataHigh[i] - dataLow[i])
    }
    return resVal.toDoubleArray()
  }

  fun getStatsOfHighVal(dataHigh: DoubleArray, dataOpen: DoubleArray, dataClose: DoubleArray): DescriptiveStatistics {
    val retVal = mutableListOf<Double>()
    for (i in dataHigh.indices){
      val larger = max(dataOpen[i], dataClose[i])
      println("$i: larger: $larger ... dataHigh ${dataHigh[i]}")
      retVal.add(dataHigh[i] - larger)
    }
    return DescriptiveStatistics(retVal.toDoubleArray())
  }

  fun getStatsOfLowVal(dataLow: DoubleArray, dataOpen: DoubleArray, dataClose: DoubleArray): DescriptiveStatistics {
    val retVal = mutableListOf<Double>()
    for (i in dataLow.indices){
      val smaller = min(dataOpen[i], dataClose[i])
      println("smaller: $smaller ... dataLow ${dataLow[i]}")
      retVal.add(smaller - dataLow[i])
    }
    return DescriptiveStatistics(retVal.toDoubleArray())
  }

}
