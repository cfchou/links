#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# adapted from http://www.timestretch.com/FractalBenchmark.html

typename Context = Int;

alien javascript jsmandelbrot : (Float, Float) ~> Int;

alien javascript getCanvasById : (String) ~> Context;
alien javascript canvasSetFillStyle : (Context, String) ~> ();
alien javascript canvasFillRect : (Context, Int, Int, Int, Int) ~> ();

alien javascript fullyNativeMandelbrot : () -> ();

var bailout = 16.0;
var max_iterations = 200;

fun makeCanvasDiv(id, height, width) {
 appendChildren(
        <div id="{id}"
             style="position: relative; float: left;
                    width: {intToString(2*width)}px;
                    height: {intToString(2*height)}px">
        </div>,
        getNodeById("body"))
}


fun plotDiv(id, colour, x, y) {
 appendChildren(
        <div style="position: absolute;
                    background-color: {colour}; 
                    width: 2px;
                    height: 2px;
                    left: {intToString(2*x)}px;
                    top: {intToString(2*y)}px"> </div>,
        getNodeById(id))
}

fun makeCanvas(id, colour, height, width) {
  appendChildren(
    <canvas id="{id}"
	    width="{intToString(2*width)}"
            height="{intToString(2*height)}">
    </canvas>,
    getNodeById("body"));
   var context = getCanvasById(id);
   canvasSetFillStyle(context, colour);
   context
}

fun plot(context, x, y) {
  canvasFillRect(context, x*2, y*2, 2, 2);
}


# process associated with a canvas.  Receive Point messages and render
# them on the screen using 2x2 div elements.
fun draw(context) client {
  receive {
    case Point(x,y) -> {
      plot(context, x, y);
    }
  };
  draw(context);
}

# Create a canvas and return its process id to the calling process.
# The canvas can receive messages of the form Point (x,y)
fun canvas (x, y, colour, id) {
  var context = makeCanvas(id, colour, x, y);
  spawn{ draw(context) }
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

fun nowt(x, y) {
 1
}

fun line(x, y) {
 if(x == y) {0}
 else {1}
}

fun block(x, y) {
 0
}


fun makefreshname(base, n) client {
  var name = base++intToString(n);
  if(isNull(getNodeById(name)))
    name
  else
    makefreshname(base, n+1)
}

fun getfreshid(base) {
  makefreshname(base, 0)
}

fun recurse(compute, c, x, y) {
  if (compute(intToFloat(x)/.40.0, intToFloat(y)/.40.0) == 0) (c ! Point (x+39,y+39))
  else ();
  if(x == 39) {
    if(y == 39) {()}
    else {
      recurse(compute, c, -39, y+1)
    }
  } else {
    recurse(compute, c, x+1, y)
  }  
}
fun recursive(compute, c) {
  recurse(compute, c, -39, -39)
}

fun iterative(compute, c) client {
  ignore(
  for (y <- range(-39, 39)) {
    ignore(
    for (x <- range(-39,39)) {
      (if (compute(intToFloat(x)/.40.0, intToFloat(y)/.40.0) == 0) (c ! Point (x+39,y+39))
       else ()); []
    }); []
  })
}

fun lookupName(bindings, s) {
  var fs = (for ((name, f) <- bindings)
        if(name == s) {[f]} else {[]});
  hd(fs)
}

fun traversals() {[("recursive", recursive), ("iterative", iterative)]}
fun drawings() {[("empty", nowt), ("line", line), ("block", block),
             ("Mandlebrot set (Links computation)", mandelbrot),
             ("Mandelbrot set (JavaScript computation)", jsmandelbrot)]}

fun dodrawing(drawingName, traversalName) client {
  var id = getfreshid("drawing");
  var c = canvas (80, 80, "red", id);
  var startTime = clientTime();


  var drawing = lookupName(drawings(), drawingName);

  var traversal = lookupName(traversals(), traversalName);

  traversal(drawing, c);

  var endTime = clientTime();
  var totalTime = (endTime-startTime);

  insertBefore(stringToXml(intToString(totalTime)++"ms"), getNodeById(id));

  debug("Time to draw "++id++": "++intToString(totalTime)++"ms")
}

# fun makeButton(name) {
#   <td>
#   <input type="submit" value="{name}" />
#   </td>
# }

#    <table><tr>
#   {for ((name, drawing) <- drawings())
#      makeButton(name)}
#    </tr></table>


# neither of these abstractions work
# because l:names have to be bound in
# the same context that they're used

# furthermore, apparently, radio buttons don't
# seem to work at all

#fun radioButtons(name, bindings) {
#  for ((x, f) <- bindings)
#    <input type="radio" l:name="{name}" value="{x}" />
#}

#fun selection(name, bindings) {
#  <select l:name="{name}">
#    {for ((x, f) <- bindings)
#       <option>{stringToXml(x)}</option>}
#  </select>
#}

#   <select l:name="traversalName">
#     {for ((name, traversal) <- traversals)
#        <option>{stringToXml(name)}</option>}
#   </select>

page
<html>
 <body>
  <h1>Mandelbrot benchmarks using the canvas API</h1>
  <form l:onsubmit="{ignore(spawn{dodrawing(drawingName, traversalName)})}">
  Traversal: 
  <select l:name="traversalName">
    {for ((name, traversal) <- traversals())
        <option>{stringToXml(name)}</option>}
  </select>
  Drawing:
  <select l:name="drawingName">
    {debug(intToString(length(drawings())));
     for ((name, drawing) <- drawings())
       <option>{stringToXml(name)}</option>}
  </select>
  <button type="submit">Draw</button>
  </form>
  <form l:onsubmit="{fullyNativeMandelbrot()}">
    <button type="submit">Draw Mandelbrot set using only JavaScript</button>
  </form>
  <div id="body"/>
 </body>
</html>


