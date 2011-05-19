#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun compute(count, total) server {
 if (count < total) {
  showProgress(count, total);
  compute(count+1, total)
 } else "done counting to " ^^ intToString(total)
}

fun showProgress(count, total) client {
 var percent = 100.0 *. intToFloat(count) /. intToFloat(total);
 replaceNode(
        <div id="bar"
             style="width:{floatToString(percent)}%;
                    background-color: black">|</div>,
        getNodeById("bar")
 )
}

fun showAnswer(answer) client {
 replaceNode(
	<div id="bar">{stringToXml(answer)}</div>,
        getNodeById("bar")       
	)
}

fun newDoc() client {
 replaceDocument(
    <html xmlns="http://www.w3.org/1999/xhtml"> 
    <body>
    <svg xmlns="http://www.w3.org/2000/svg" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:svg="http://www.w3.org/2000/svg" id="canvas"
    width="800px" height="600px" >
        <circle cx="60px" cy="100px" r="50px"
        style="fill:white; stroke:red; stroke-width:4" />
    </svg>
    </body>
    </html>)
}

page
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style>
    #svgbasics {{ width: 100px; height: 50px; border: 1px solid #484; }}
</style>
</head>

<body>
   <form l:onsubmit="{showAnswer(compute(0, stringToInt(n)))}">
    <input type="text" l:name="n"/>
    <input type="submit"/>
   </form>
   <div id="bar"/>


<div id="svgbasics">
   <a l:onclick="{swapNodes(getNodeById("obj1"), getNodeById("frm1"))}">swap</a>
   <a l:onclick="{newDoc()}">replace</a>
</div>

<object id="obj1" data="../test.svg" type="image/svg+xml" width="400" height="300">object</object>
<iframe id="frm1" src="../test.svg" style="color: purple" width="240" height="100" seamless="seamless"/>

<svg width="12cm" height="3.6cm" viewbox="0 0 1000 300">
    <circle cx="60px" cy="100px" r="50px"
    style="fill:white; stroke:red; stroke-width:4" />
</svg>
</body>
 </html>
