#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# adapted from http://www.timestretch.com/FractalBenchmark.html

var bailout = 16.0;
var max_iterations = 200;

# process associated with a canvas.  Receive Point messages and render
# them on the screen using 2x2 div elements.
fun draw(colour, id) client {
  receive {
    case Point(x,y) ->
     appendChildren(
                 <div style="position: absolute;
                             background-color: {colour}; 
                             width: 2px;
                             height: 2px;
                             left: {intToString(2*x)}px;
                             top: {intToString(2*y)}px"> </div>,
                 getNodeById(id))
  };
  draw(colour, id)
}

# Create a canvas and return its process id to the calling process.
# The canvas can receive messages of the form Point (x,y)
fun canvas (x, y, colour, id) {
  appendChildren(
              <div id="{id}"
                   style="position: relative;
                          float: left; width: {intToString(2*x)}px;
                          height: {intToString(2*y)}px"> </div>,
              getNodeById("body"));
  spawn{ draw(colour, id) }
}

fun range(f, to) {
  if (f >= to) []
  else f :: range(f+1, to)
}

fun mandelbrot(x, y) {
  var cr = y -. 0.5;
  var ci = x;
  var zi = 0.0;
  var zr = 0.0;
  var i = 0;
  fun loop(zr, zi, i) {
      var i = i + 1;
      var temp = zr *. zi;
      var zr2 = zr *. zr;
      var zi2 = zi *. zi;
      var zr = zr2 -. zi2 +. cr;
      var zi = temp +. temp +. ci;
      if (zi2 +. zr2 > bailout)  i
      else if (i > max_iterations) 0
      else loop(zr, zi, i)
  }
  loop(zr, zi, i)
}

fun makefreshname(colour, n) client {
  var name = colour ^^ intToString(n);
  if(isNull(getNodeById(name)))
    name
  else
    makefreshname(colour, n+1)
}

fun getfreshid(colour) {
  makefreshname(colour, 0)
}

fun iterate(colour) client {
  var id = getfreshid(colour);
  var c = canvas (80, 80, colour, id);
  for (y <- range(-39, 39)) {
    ignore(
    for (x <- range(-39,39)) {
      (if (mandelbrot(intToFloat(x)/.40.0, intToFloat(y)/.40.0) == 0) (c ! Point (x+39,y+39))
       else ()); []
    }); []
  }
}

var colours = ["red", "green", "blue", "black", "orange", "purple"];

page
 <html>
  <body>
   <select l:onchange="{ignore(spawn{iterate(getTargetValue(event))})}"
 	style="display: block">
     {for (colour <- colours)
        <option>{stringToXml(colour)}</option>}
   </select>
   <div id="body"/>
  </body>
 </html>


