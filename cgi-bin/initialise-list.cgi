#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
var db = database "draggable";
#var db = database "draggable";
var itemsTable = table "items" with (i : Int, name : String) from db;

### library functions ###
fun upto(i,j) {
  if(j < i) {
    []
  } else {
    i :: (upto(i+1, j))
  }
}

fun map(f, xs) {
  switch (xs) {
    case [] -> []
    case (x::xs) -> f(x) :: (map(f, xs))
  }
}

fun foldr(f, xs, y) {
  switch (xs) {
    case [] -> y
    case (x::xs) -> foldr(f, xs, f(x,y))
  }
}

fun filter(xs, p) {
  foldr(
    fun(x,ys) {
     if(p(x)) {x :: ys}
     else {ys}
    }, xs, [])
}

fun mem(y, xs) {
  not (filter (xs, fun (x) {x == y}) == [])
}

fun diff(xs,ys) {
  filter(xs, fun (x) {not(mem(x, ys))})
}

fun product(xs) {
  foldr ((*), xs, 1)
}
### end of library functions ###

#fun select(xs, i) {
#  var n = length(xs);
#  if (i < 0 || n <= i) {
#    error("list index " ^^ intToString(i) ^^ " out of range [0.."
#          ^^ intToString(n) ^^ ")")
#  } else {
#    fun sel(xs, i) {
#      switch (xs, i) {
#        case (x::xs, 0) -> x; 
#        case (x::xs, i) -> sel(xs, i-1);
#        case ([], i) -> error ("unreachable");
#      }
#    }
#    sel(xs, i)
#  }
#}

fun select(xs, i) {
  hd(drop(i, xs))
}

fun insertItems(itemsTable, itemsList) {
  var n = length(itemsList);
  
  ignore(mapi(
    fun (item, i) {
      update (r <-- itemsTable)
        where (r.i == i)
          set (name=item)
    },
    itemsList));
  delete (itemEntry <-- itemsTable)
    where (itemEntry.i < 0 || n < itemEntry.i);
  var indexes = for (itemEntry <- asList(itemsTable)) [itemEntry.i];
  insert itemsTable values (i, name)
    for (i <- upto(0,n-1) `diff` indexes)
      [(i=i, name=select(itemsList, i))];
}

# `diff` is list difference

insertItems(itemsTable, ["Pooh", "Paddington", "Rupert", "Edward"]) 

