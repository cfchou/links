#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun append() client {
 var deck = domGetRefById("deck");
 var newJoke = <ul><li> Q: Why don't Buddhists vacuum in the corners?</li>
               <li> A: Because they have no attachments. </li> </ul>;
 domAppendChild(newJoke, deck)
}

fun appendToDoc() client {
 var doc = domGetDocumentRef();
 var choreList = <ul id="chores"><li>laundry</li>
                             <li>fix bike</li></ul>;
 domAppendChild(choreList, doc)
}

fun remove() client {
  var chores = domGetRefById("chores");
  domRemoveRef(chores)
}

fun removeDoc() client {
  var doc = domGetDocumentRef();
  domRemoveRef(doc)
}

fun move() client {
  var setup = domGetRefById("setup");
  var punchline = domGetRefById("punchline");
  domInsertBeforeRef(punchline, setup)
}

fun moveAppend() client {
  var deck = domGetRefById("deck");
  var punchline = domGetRefById("punchline");
  domAppendChildRef(punchline, deck)
}

fun representation() client {
  var deckRef = domGetRefById("deck");
  var deckXml = domGetXml(deckRef);
  var doc = domGetDocumentRef();
  domAppendChild(deckXml,doc)
}

fun deckTagName() {
  var deck = domGetRefById("deck");
  var deckXml = domGetXml(deck);
  debug(getTagName(deckXml))
}

fun deckStyle() {
  var deck = domGetRefById("deck");
  var deckXml = domGetXml(deck);
  debug(getAttribute(deckXml, "style"))
}

<html>
 <body>
  <a l:onclick="{appendToDoc()}">Append Chores</a>
  <a l:onclick="{remove()}">Remove Chores</a>
  <a l:onclick="{append()}">Append Extra Punchline</a>
  <a l:onclick="{move()}">Move punchline before setup</a>
  <a l:onclick="{moveAppend()}">Move punchline to end</a>
  <a l:onclick="{representation()}">Copy deck using XML rep'n</a>
  <a l:onclick="{deckTagName()}">What is the tag name on `deck'?</a>
  <a l:onclick="{deckStyle()}">What is the style of `deck'?</a>
  <div id="deck" style="border: 1px solid black">
    <h1 id="setup">A Buddhist walks up to a hot dog stand.</h1>
    <p id="punchline">He says, "Can you make me one with everything?"</p>
  </div>
 </body>
</html>
