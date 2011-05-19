#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# div-based drawing.

# Create a canvas and return its id to the calling process.
# The canvas can receive messages of the form Point (x,y)
fun canvas (x, y, id) {
  appendChildren(
         <div id="{id}"
              style="width: {intToString(x)}px;
                     height: {intToString(y)}px"> </div>,
         getNodeById("body"));
  spawn{ draw(id) }
}

# process associated with a canvas.  Receive Point messages and render
# them on the screen using 2x2 div elements.
fun draw(id) client {
  receive {
    case Point(x,y) -> {
     appendChildren(
               <div style="position: absolute;
                           background-color: red; 
                           width: 1px;
                           height: 1px;
                           left: {intToString(x)}px;
                           top: {intToString(y)}px"> </div>,
               getNodeById(id))
    }
  };
  draw(id)
}

# [a..b]
fun range(f, to) {
  if (f >= to) []
  else f :: range(f+1, to)
}

fun scribble() {
  var c = canvas (100,100, "pad");
  ignore(for (i <- range(0,50))
    for (j <- range(0,50))
      [c ! Point(i*2,j*2)]);
}

page
 <html><body>
   <div id="body"/>
   <a l:onclick="{scribble()}">draw</a>
 </body></html>
