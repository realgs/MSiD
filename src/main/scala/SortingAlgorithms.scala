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

  println(insertSort(List(6, 1, 125, 76, 14, 5, 1, 1, 6, 1, 6, 8, 8, 5, 3)))
  println(selectionSort(List(6, 1, 125, 76, 14, 5, 1, 1, 6, 1, 6, 8, 8, 5, 3)))
}
