#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun waiting(id) client {
 receive {
  case MouseDown(elem)  ->
   if (isElementNode(elem) && (parentNode(elem) == getNodeById(id)))
    dragging(id, elem)
   else
    waiting(id)
  case MouseUp          -> waiting(id)
  case MouseOut(toElem) -> waiting(id)
 }
}

fun dragging(id, elem) client {
 receive {
  case MouseUp          -> waiting(id)
  case MouseDown(elem)  ->
   if (isElementNode(elem) && (parentNode(elem) == getNodeById(id)))
    dragging(id, elem)
   else
    waiting(id)
  case MouseOut(toElem) ->
   if (isElementNode(toElem) && (parentNode(toElem) == getNodeById(id))) {
    swapNodes(elem, toElem);
    dragging(id, elem)
   } else dragging(id, elem)
 }
}

fun format(text) {
    <li style="color: #7E9E50; font: 20px Georgia; background-color: #ECF3E1; 
               border:1px solid #C5DEA1; cursor: move; margin: 0px;">
    {stringToXml(text)}</li>
}

fun draggableList(id, items)
{
  var x = id;
  var dragger = spawn { waiting(id) };
   <ul id="{id}" style="width: 200px; 
        list-style-image: url(http://script.aculo.us/images/bullet.gif)"
      l:onmouseup   = "{dragger ! MouseUp}"
      l:onmouseuppage = "{dragger ! MouseUp}"
      l:onmousedown = "{dragger ! MouseDown(getTarget(event))}"
      l:onmouseout  = "{dragger ! MouseOut(getToElement(event))}"
   >
    {for (item <- items)
         format(item)}
  </ul>

}

page
 <html>
 <body>
 <h2 style="font: 42px/30px Georgia, serif; color: #7E9E50;">Great Bears</h2>
 {draggableList("bears",["Pooh", "Paddington", "Rupert", "Edward"])}
 <h2 style="font: 42px/30px Georgia, serif; color: #7E9E50;">Great Beers</h2>
 {draggableList("beers",["Budvar", "Delirium Tremens", "Deuchars"])}
 <h2 style="font: 42px/30px Georgia, serif; color: #7E9E50;">Great Boars</h2>
 {draggableList("boars",["Sus scrofa scrofa","Sus scrofa ussuricus",
                         "Sus scrofa cristatus","Sus scrofa taiwanus"])}
 </body>
 </html>

