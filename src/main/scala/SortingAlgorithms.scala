import scala.annotation.tailrec

object SortingAlgorithms extends App {
  def maximum(xs: List[Int]): List[Int] =
    (xs.tail foldLeft List(xs.head)) {
      (ys, x) =>
        if(x > ys.head) (x :: ys)
        else (ys.head :: x :: ys.tail)
    }

  def selectionSort(xs: List[Int]) = {
    def selectionSortHelper(xs: List[Int], accumulator: List[Int]): List[Int] =
      if(xs.isEmpty) accumulator
      else {
        val ys = maximum(xs)
        selectionSortHelper(ys.tail, ys.head :: accumulator)
      }

    selectionSortHelper(xs, Nil)
  }

  def insertSort(xs: List[Int]): List[Int] =
    xs match {
      case Nil => Nil
      case h::t =>  insert(h, insertSort(t))
    }

  def insert(x: Int, xs: List[Int]): List[Int] =
    (x,xs) match {
      case (_,h::_) if x<=h => x :: xs
      case (_,h::t) =>  h :: insert(x, t)
      case _ => x::Nil
    }
  def bubblesort(source: List[Int]) : List[Int]  = {
    @tailrec
    def sort(iteration: List[Int], source: List[Int] , result: List[Int]) : List[Int]= source match {
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
        val (part1, part2) = split(list) //list.splitAt(list.length / 2)
        val sorted1 = mergeSort(part1)
        val sorted2 = mergeSort(part2)
        merge(sorted1, sorted2)
    }
  println(bubblesort(List(6, 1, 125, 76, 14, 5, 1, 1, 6, 1, 6, 8, 8, 5, 3)))
  println(insertSort(List(6, 1, 125, 76, 14, 5, 1, 1, 6, 1, 6, 8, 8, 5, 3)))
  println(selectionSort(List(6, 1, 125, 76, 14, 5, 1, 1, 6, 1, 6, 8, 8, 5, 3)))
}
