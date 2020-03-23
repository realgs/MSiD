import scala.annotation.tailrec
import scala.util.Random

object SortingAlgorithms extends App {
  def maximum[T <% Ordered[T]](xs: List[T]): List[T] =
    (xs.tail foldLeft List(xs.head)) {
      (ys, x) =>
        if(x > ys.head) (x :: ys)
        else (ys.head :: x :: ys.tail)
    }

  def selectionSort[T <% Ordered[T]](xs: List[T]) = {
    def selectionSortHelper(xs: List[T], accumulator: List[T]): List[T] =
      if(xs.isEmpty) accumulator
      else {
        val ys = maximum(xs)
        selectionSortHelper(ys.tail, ys.head :: accumulator)
      }

    selectionSortHelper(xs, Nil)
  }

  def insertSort[T <% Ordered[T]](xs: List[T]): List[T] =
    xs match {
      case Nil => Nil
      case h::t =>  insert(h, insertSort(t))
    }

  def insert[T <% Ordered[T]](x: T, xs: List[T]): List[T] =
    (x,xs) match {
      case (_,h::_) if x<=h => x :: xs
      case (_,h::t) =>  h :: insert(x, t)
      case _ => x::Nil
    }
  def bubbleSort[T <% Ordered[T]](source: List[T]) : List[T]  = {
    @tailrec
    def sort(iteration: List[T], source: List[T] , result: List[T]) : List[T]= source match {
      case h1 :: h2 :: rest => if(h1 > h2) sort(iteration, h1 :: rest, result :+ h2) else sort(iteration, h2 :: rest, result :+ h1)
      case l:: Nil => sort(iteration, Nil, result :+ l)
      case Nil => if(iteration.isEmpty) return result else sort(iteration.dropRight(1), result, Nil )
    }
    sort(source,source,Nil)
  }
  def split[T <% Ordered[T]](list: List[T]): (List[T], List[T]) =
    list match {
      case Nil => (Nil, Nil)
      case head :: Nil => (head :: Nil, Nil)
      case first :: second :: tail =>
        val (tl1, tl2) = split(tail)
        (first :: tl1, second :: tl2)
    }

  def merge[T <% Ordered[T]](list1: List[T], list2: List[T]): List[T] =
    (list1, list2) match {
      case (x, Nil) => x
      case (Nil, y) => y
      case (flh :: flt, slh :: slt) =>
        if (flh > slh)
          slh :: merge(list1, slt)
        else
          flh :: merge(flt, list2)
    }

  def mergeSort[T <% Ordered[T]](list: List[T]): List[T] =
    list match {
      case Nil | _ :: Nil =>
        list
      case _ =>
        val (part1, part2) = split(list)
        val sorted1 = mergeSort(part1)
        val sorted2 = mergeSort(part2)
        merge(sorted1, sorted2)
    }

  def time[R](block: => R): Any = {
    val t0 = System.nanoTime()
    block
    val t1 = System.nanoTime()
    println("Elapsed time: " + (t1 - t0)*Math.pow(10,-9) + "s")
  }
  def r = new Random();
  time(insertSort((1 to 1000 map r.nextInt).toList))
  time(selectionSort((1 to 1000 map r.nextInt).toList))
  time(mergeSort((1 to 1000 map r.nextInt).toList))
  time(bubbleSort((1 to 1000 map r.nextInt).toList))


}
