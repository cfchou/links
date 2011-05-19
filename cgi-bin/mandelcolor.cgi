#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
var precision = 10.0;
var realUnit = precision;

fun zmagsq(c) {
  var r = c.1; var i = c.2;
  (r*.r +. i*.i) /. precision
}

fun zsquare(c) {
  var r = c.1; var i = c.2;
  ((r *. r -. i *. i)/.precision, (2.0 *. r *. i)/.precision)
}

#fun zplus((r1, i1), (r2, i2)) {
#  (r1 + r2, i1 + i2)
#}
fun zplus(z1, z2) {
  (z1.1 +. z2.1, z1.2 +. z2.2)
}

var the_limit = 16.0;

fun mandelloop(c, z, i) {
  if (zmagsq(c) > precision) {
    i
  } else if (i >= the_limit) {
    i
  } else {
    mandelloop(zplus(z, zsquare(c)), z, i+.1.0)
  }
}

fun mandelbrot(r, i, limit) {
  # c <- z + c^2
  var c = (0.0, 0.0);
  var z = (r, i);
  mandelloop(c, z, 0.0)
}

fun mandelmatrix(r, i, result, minr, maxr, mini, maxi) {
  if (i >= maxi) {
    result
  } else {
    if (r >= maxr) {
      if (i+.1.0 >= maxi) result
      else 
        mandelmatrix(minr, i+.1.0, []::result, minr, maxr, mini, maxi)
    } else {
      var point = mandelbrot(r, i, the_limit);
      var result = (point :: hd(result)) :: tl(result);
      mandelmatrix(r+.1.0, i, result, minr, maxr, mini, maxi)
    }
  }
}

fun mandelregion(minr, maxr, mini, maxi) {
  mandelmatrix(minr, mini, [[]], minr, maxr, mini, maxi)
}

fun hexdigit(i) {
  switch (floatToInt(i)) {
    case 0 -> "0"
    case 1 -> "1"
    case 2 -> "2"
    case 3 -> "3"
    case 4 -> "4"
    case 5 -> "5"
    case 6 -> "6"
    case 7 -> "7"
    case 8 -> "8"
    case 9 -> "9"
    case 10 -> "a"
    case 11 -> "b"
    case 12 -> "c"
    case 13 -> "d"
    case 14 -> "e"
    case _ -> "f"
  }
}

fun redshade(i, max) {
  if (i == max) "#000"
  else
    "#" ^^ hexdigit(16.0*.i/.max) ^^ "33"
  
}

fun pixeldiv(x, y, size, color) {
  var size = intToString(floatToInt(size));
  var x = intToString(floatToInt(x));
  var y = intToString(floatToInt(y));
  <div id="{"p" ^^ x ^^ "x" ^^ y}"
       style="width: {size}px; 
              height: {size}px;
              position: absolute;
              left: {x}px;
              top: {y}px;
              background-color: {redshade(color, the_limit)}"> </div>
}

fun numbers(start, l) {
  if (l == []) []
  else
    (start, hd(l)) :: numbers(start+.1.0, tl(l))
}

sig mandelBlock : (Float, Float, Float, Float, Float, Float) ~> Xml
fun mandelBlock(pixSize, x, y, regionSize, r, i) {
  var halfPixSize = pixSize /. 2.0;
  pixeldiv(x, y, halfPixSize, mandelbrot(r, i, the_limit)) ++
   pixeldiv(x+.(halfPixSize), y, halfPixSize, mandelbrot(r+.regionSize, i, the_limit)) ++
   pixeldiv(x, y+.(halfPixSize), halfPixSize, mandelbrot(r, i+.regionSize, the_limit)) ++
   pixeldiv(x+.(halfPixSize), y+.(halfPixSize), halfPixSize, mandelbrot(r+.regionSize, i+.regionSize, the_limit))
}

fun dilation(mina, minb, maxa, maxb, minc, mind, maxc, maxd)
{
  ((maxc -. minc) /. (maxa -. mina),
   (maxd -. mind) /. (maxb -. minb))
}

fun mandelMadness(x, y, r, i, pixSize,
                  minx, miny, maxx, maxy,
                  mini, minr, maxi, maxr)
{
  var (xdil, ydil) = dilation(minx, miny, maxx, maxy,
                          mini, minr, maxi, maxr);
  var regionSize = pixSize *. xdil;
  if (x >= maxx) {
    if (y >= maxy) {
      if (pixSize <= 1.0) {
        ()
      } else {
        mandelMadness(minx, miny, minr, mini, pixSize/.2.0,
                      minx, miny, maxx, maxy, 
                      mini, minr, maxi, maxr)
      }
    } else {
      mandelMadness(minx, y+.pixSize, minr, i+.regionSize, pixSize,
                    minx, miny, maxx, maxy,
                    mini, minr, maxi, maxr);
    }
  } else {
    if (y >= maxy) {
      mandelMadness(minx, miny, minr, mini, pixSize/.2.0,
                    minx, miny, maxx, maxy, 
                    mini, minr, maxi, maxr)
    } else {
      var docElt = getDocumentNode();
      appendChildren(mandelBlock(pixSize, x, y,
                                     regionSize, r, i), docElt);
      mandelMadness(x+.pixSize, y, r+.regionSize, i, pixSize,
                    minx, miny, maxx, maxy,
                    mini, minr, maxi, maxr);
    }
  }
}

fun goMandelMadness(mini, minr, maxi, maxr, pixelWidth)
{
  mandelMadness(0.0, 0.0, minr, mini, pixelWidth,
                0.0, 0.0, pixelWidth, pixelWidth, 
                mini, minr, maxi, maxr)
}

fun main() client {
  replaceDocument(
  <html><body>
    <div id="p0x0" />
  </body></html>);
  goMandelMadness(-.1.0 *. realUnit, -.1.0 *. realUnit, realUnit, realUnit, 512.0);

  # insane hack
  page <#/>
}

main()
