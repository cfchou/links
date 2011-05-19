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

page
 <html>
  <body>
   <form l:onsubmit="{showAnswer(compute(0, stringToInt(n)))}">
    <input type="text" l:name="n"/>
    <input type="submit"/>
   </form>
   <div id="bar"/>
  </body>
 </html>
