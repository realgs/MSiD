import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.random.Random

class Simulator(dataset: List<ChartData>) {

  private val highData: DoubleArray = dataset.map { it.high }.toDoubleArray()
  private val lowData: DoubleArray = dataset.map { it.low }.toDoubleArray()
  private val openData: DoubleArray = dataset.map { it.open }.toDoubleArray()
  private val closeData: DoubleArray = dataset.map { it.close }.toDoubleArray()
  private val volumeData: DoubleArray = dataset.map { it.volume }.toDoubleArray()

  private val closeChangeData: DoubleArray = getChangeData(closeData)

  var correction = 0.0

  fun averageSimulation(numOfIterations: Int) {
    val allData = mutableListOf<MutableList<ChartData>>()
    for (i in 0 until numOfIterations) {
      allData.add(simulate())
    }

    val averageCloses = mutableListOf<Double>()
    val averageVolumes = mutableListOf<Double>()

    for (i in allData.first().indices) {
      averageCloses.add(allData.sumByDouble { it[i].close } / numOfIterations)
      averageVolumes.add(allData.sumByDouble { it[i].volume } / numOfIterations)
    }

    val averageOpens = setNewOpens(highData.last(), averageCloses)
    val averageHighs = generateNewHigh(openData, closeData, averageOpens, averageCloses)
    val averageLows = generateNewLow(openData, closeData, averageOpens, averageCloses)

    val newValues = mutableListOf<ChartData>()

    for (i in 0 until averageHighs.size) {
      newValues.add(ChartData(averageHighs[i], averageLows[i], averageOpens[i], averageCloses[i], averageVolumes[i]))
    }

    ChartCanvas("Average", newValues)

    println("Average close mean: ${DescriptiveStatistics(averageCloses.toDoubleArray()).mean} ::: Average close standard deviation: ${DescriptiveStatistics(averageCloses.toDoubleArray()).standardDeviation}")
    println("Average volume mean: ${DescriptiveStatistics(averageVolumes.toDoubleArray()).mean} ::: Average volume standard deviation: ${DescriptiveStatistics(averageVolumes.toDoubleArray()).standardDeviation}")

  }

  fun simulate(): MutableList<ChartData> {

    correction = 0.0

    val dsClose = DescriptiveStatistics(closeData)
    val dsVolume = DescriptiveStatistics(volumeData)

    val dsCloseChange = DescriptiveStatistics(closeChangeData)
    val dsVolumeChange = DescriptiveStatistics(volumeData)

    val newValues: MutableList<ChartData> = mutableListOf()

    val deviationDataClose = getValuesOutsideStandardDeviation(closeData, dsClose)
    val deviationDataVolume = getValuesOutsideStandardDeviation(volumeData, dsVolume)

    val newClose = generateNewVal(closeData.last(), closeData.size, dsClose, dsCloseChange, deviationDataClose, mutableListOf())
    val newOpen = setNewOpens(closeData.last(), newClose)

    val newHigh = generateNewHigh(openData, closeData, newOpen, newClose)
    val newLow = generateNewLow(openData, closeData, newOpen, newClose)

    correction = 0.0

    val newVolume = generateNewVal(volumeData.last(), volumeData.size, dsVolume, dsVolumeChange, deviationDataVolume, mutableListOf())

    for (i in 0 until newHigh.size) {
      newValues.add(ChartData(newHigh[i], newLow[i], newOpen[i], newClose[i], newVolume[i]))
    }

    return newValues

  }

  fun generateNewHigh(openData: DoubleArray, closeData: DoubleArray, newOpenData: MutableList<Double>, newCloseData: MutableList<Double>): MutableList<Double> {
    val dsHighData = getStatsOfHighVal(highData, openData, closeData)
    val retVal = mutableListOf<Double>()
    for (i in openData.indices) {
      val larger = max(newOpenData[i], newCloseData[i])
      val d100roll = Random.nextInt(0, 100)
      retVal.add(larger + ((dsHighData.mean + dsHighData.standardDeviation) / 100) * d100roll)
    }
    return retVal
  }

  fun generateNewLow(openData: DoubleArray, closeData: DoubleArray, newOpenData: MutableList<Double>, newCloseData: MutableList<Double>): MutableList<Double> {
    val dsLowData = getStatsOfLowVal(lowData, openData, closeData)
    val retVal = mutableListOf<Double>()
    for (i in openData.indices) {
      val smaller = min(newOpenData[i], newCloseData[i])
      val d100roll = Random.nextInt(0, 100)
      retVal.add(smaller - ((dsLowData.mean + dsLowData.standardDeviation) / 100) * d100roll)
    }
    return retVal
  }


  fun setNewOpens(firstVal: Double, closeData: MutableList<Double>): MutableList<Double> {
    val retVal = mutableListOf<Double>()
    retVal.add(firstVal)
    for (close in closeData) {
      retVal.add(close)
    }
    return retVal.dropLast(1).toMutableList()
  }

  fun generateNewVal(prevVal: Double, threshold: Int, ds: DescriptiveStatistics, dsc: DescriptiveStatistics, deviationData: Pair<DoubleArray, DoubleArray>, acc: MutableList<Double>): MutableList<Double> {
    val dsValuesAboveDev = deviationData.first
    val dsValuesBelowDev = deviationData.second
    val newVal = generateValue(ds, dsc, dsValuesAboveDev, dsValuesBelowDev, prevVal)
    acc.add(newVal)
    if (threshold > 0) generateNewVal(newVal, threshold - 1, ds, dsc, deviationData, acc)
    return acc
  }

  fun generateValue(ds: DescriptiveStatistics, dsChange: DescriptiveStatistics, valsAboveDev: DoubleArray, valsBelowDev: DoubleArray, previousValue: Double): Double {
    var growChance = 50.0

    val dsValAboveStat = DescriptiveStatistics(valsAboveDev)
    val dsValBelowStat = DescriptiveStatistics(valsBelowDev)

    if (previousValue > ds.mean) {
      var divider = dsValAboveStat.mean + dsValAboveStat.standardDeviation - ds.mean
      if (divider == 0.0 || divider.isNaN()) divider = ds.mean + ds.max
      growChance = 100.0 - (previousValue - ds.mean) / divider * 100
    } else if (previousValue < ds.mean) {
      var divider = ds.mean - dsValBelowStat.mean - dsValBelowStat.standardDeviation
      if (divider == 0.0 || divider.isNaN()) divider = ds.mean - ds.min
      growChance = (ds.mean - previousValue) / divider * 100
    }

    val d100Roll = Random.nextInt(0, 100)

    if (growChance - d100Roll > 0) {
      val newVal = previousValue + rollNewVal(dsChange, dsValAboveStat) - correction
      if (newVal < 0) {
        val retVal = ds.min
        correction = abs(newVal) - ds.min
        return retVal
      }
      return newVal
    } else if (growChance - d100Roll < 0) {
      val newVal = previousValue - rollNewVal(dsChange, dsValBelowStat) - correction
      if (newVal < 0) {
        val retVal = ds.min
        correction = abs(newVal) - ds.min
        return retVal
      }
      return newVal
    }
    return previousValue
  }

  fun rollNewVal(dsc: DescriptiveStatistics, dsCh: DescriptiveStatistics): Double {
    val changeRoll = Random.nextInt(0, 100)
    return ((dsc.mean + dsc.standardDeviation) / 100) * changeRoll
  }

  fun getValuesOutsideStandardDeviation(data: DoubleArray, ds: DescriptiveStatistics): Pair<DoubleArray, DoubleArray> {
    val above = mutableListOf<Double>()
    val below = mutableListOf<Double>()
    data.forEach {
      if (it > ds.mean + ds.standardDeviation) {
        above.add(it)
      } else if (it < ds.mean - ds.standardDeviation) {
        below.add(it)
      }
    }
    return Pair(above.toDoubleArray(), below.toDoubleArray())
  }

  fun getChangeData(data: DoubleArray): DoubleArray {
    val resVal = mutableListOf<Double>()
    for (i in 1 until data.size) {
      resVal.add(abs(data[i] - data[i - 1]))
    }
    return resVal.toDoubleArray()
  }

  fun getStatsOfHighVal(dataHigh: DoubleArray, dataOpen: DoubleArray, dataClose: DoubleArray): DescriptiveStatistics {
    val retVal = mutableListOf<Double>()
    for (i in dataHigh.indices) {
      val larger = max(dataOpen[i], dataClose[i])
      retVal.add(dataHigh[i] - larger)
    }
    return DescriptiveStatistics(retVal.toDoubleArray())
  }

  fun getStatsOfLowVal(dataLow: DoubleArray, dataOpen: DoubleArray, dataClose: DoubleArray): DescriptiveStatistics {
    val retVal = mutableListOf<Double>()
    for (i in dataLow.indices) {
      val smaller = min(dataOpen[i], dataClose[i])
      retVal.add(smaller - dataLow[i])
    }
    return DescriptiveStatistics(retVal.toDoubleArray())
  }

}
