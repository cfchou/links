#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# This program is intended to execute all the client-side primitive
# functions, to ensure that they are defined. It doesn't presently cover
# all the primitives, but it probably should. One day, it could test
# the functions' behaviors, checking return values and such.
# The list of function signatures in comments was dumped May 24, 07

fun test() {

ignore (1 == 1);

var (1=x|r) = (1,2,3);

# +                : (Int, Int) -> Int
# -                : (Int, Int) -> Int
# *                : (Int, Int) -> Int
# /                : (Int, Int) -> Int
# ^                : (Int, Int) -> Int
# mod              : (Int, Int) -> Int
# +.               : (Float, Float) -> Float
# -.               : (Float, Float) -> Float
# *.               : (Float, Float) -> Float
# /.               : (Float, Float) -> Float
# ^.               : (Float, Float) -> Float
#

# replaceDocument  : (Xml) -> ()

replaceDocument(<body><div id="node"></div></body>);

# stringToInt      : (String) -> Int

ignore(stringToInt("foo"));

# intToFloat       : (Int) -> Float

ignore(intToFloat(5));

# intToString      : (Int) -> String

ignore(intToString(7));

# floatToString    : (Float) -> String

ignore(floatToString(3.14));

# floatToXml    : (Float) -> Xml

# ignore(floatToXml(3.14));  # FIXME: this is broken?

# stringToFloat    : (String) -> Float

ignore(stringToFloat("2.717"));

# stringToXml      : (String) -> Xml

ignore(stringToXml("Heading"));

# intToXml         : (Int) -> Xml

ignore(intToXml(77));

# exit             : (c) -> a

#exit(1);

# spawn            : (() -{c}-> b) -> Mailbox (c)
# send             : (Mailbox (b), b) -{a}-> ()
# recv             : () -{a}-> a

var pid = spawn { ignore(recv()); };
ignore(send(pid, 1));

# self             : () -{a}-> Mailbox (a)

ignore(self());

# hd               : ([b]) -> b

ignore(hd([9,5,4,1]));

# tl               : ([b]) -> [b]

ignore(tl([9,5,4,1]));

# length           : ([b]) -> Int

ignore(length([77, 88, 102]));

# take             : (Int, [b]) -> [b]

ignore(take(4, [1, 2, 3, 4, 5, 6, 7, 8, 9]));

# drop             : (Int, [b]) -> [b]

ignore(drop(4, [1, 2, 3, 4, 5, 6, 7, 8, 9]));

# max              : ([b]) -> [|None:()|Some:b|]

ignore(max([6, 1, 4, 9, 1, 9]));

# min              : ([b]) -> [|None:()|Some:b|]

ignore(min([6, 1, 4, 9, 1, 9]));

# childNodes       : (Xml) -> Xml

var xml = <div class="section"> <h3>Heading</h3> fun </div>;

# ignore(childNodes(xml));

# objectType       : (b) -> String

ignore(objectType(<br />));

# attribute        : (Xml, String) -> [|None:()|Some:String|]

ignore(attribute(xml, "class"));

# alertDialog      : (String) -> ()

ignore(alertDialog("Testing alertDialog"));

# debug            : (String) -> ()

ignore(debug("This is a debug message."));

# debugObj         : (b) -> ()

ignore(debugObj(xml));

# dump             : (b) -> ()

ignore(dump(xml));

# print            : (String) -> ()

ignore(print("monkeys"));

# javascript       : Bool

# not              : (Bool) -> Bool

ignore(not(true));

# negate           : (Int) -> Int

ignore(negate(-7));

# negatef          : (Float) -> Float

ignore(negatef(7.5));

# getNodeById      : (String) -> DomNode

var node = getNodeById("node");

# textContent      : (DomNode) -> String

ignore(textContent(node));

# isElementNode    : (DomNode) -> Bool

ignore(isElementNode(node));

# insertBefore     : (Xml, DomNode) -> ()

insertBefore(<h1>hi</h1>, node);

# appendChildren   : (Xml, DomNode) -> ()

appendChildren(<ul id="list"><li id="item">Child 1</li></ul>, node);

# replaceNode      : (Xml, DomNode) -> ()

replaceNode(<li id="item">Replacement item</li>, getNodeById("item"));

# domInsertBeforeRef : (DomNode, DomNode) -> ()

# domInsertBeforeRef(___, node);

# domAppendChildRef : (DomNode, DomNode) -> ()

# domAppendChildRef(_,_);

# replaceChildren  : (Xml, DomNode) -> ()

replaceChildren(<#><li id="item:1">Foo</li>
                   <li id="item:2">Bar</li>
                   <li id="item:3">Baz</li></#>,
                getNodeById("list"));

# removeNode       : (DomNode) -> ()

removeNode(getNodeById("item:3"));

# swapNodes        : (DomNode, DomNode) -> ()

swapNodes(getNodeById("item:1"),getNodeById("item:2"));

# getDocumentNode  : () -> DomNode
# getValue         : (DomNode) -> Xml
# isNull           : (DomNode) -> Bool
# getTagName       : (Xml) -> String
# getTextContent   : (Xml) -> String
# getAttributes    : (Xml) -> [(String, String)]
# hasAttribute     : (Xml, String) -> Bool
# getAttribute     : (Xml, String) -> String
# getChildNodes    : (Xml) -> Xml
# domGetNodeValueFromRef : (DomNode) -> String
# domGetTagNameFromRef : (DomNode) -> String
# domGetAttributeFromRef : (DomNode, String) -> String
# domSetAttributeFromRef : (DomNode, String, String) -> String
# domGetStyleAttrFromRef : (DomNode, String) -> String
# domSetStyleAttrFromRef : (DomNode, String, String) -> String
# parentNode       : (DomNode) -> DomNode
# firstChild       : (DomNode) -> DomNode
# nextSibling      : (DomNode) -> DomNode
# getTarget        : (Event) -> DomNode
# getTargetValue   : (Event) -> String
# getTargetElement : (Event) -> DomNode
# getPageX         : (Event) -> Int
# getPageY         : (Event) -> Int
# getFromElement   : (Event) -> DomNode
# getToElement     : (Event) -> DomNode
# getTime          : (Event) -> Int
# getCharCode      : (Event) -> Char
# event            : Event
# setCookie        : (String, String) -> a

setCookie("username","frobulous t. vanderbilt");

# getCookie        : (String) -> String

#ignore(alertDialog("username cookie is: " ^^ getCookie("username")));
ignore(getCookie("username"));

# redirect         : (String) -> ()

# redirect("http://www.google.com/");

# reifyK           : ((d) -> b) -> String

# ignore(escape e in { reifyK(e) }); # not avail. on client

# sleep            : (Int) -> ()

sleep(1);

# serverTime   : () -> Int

ignore(serverTime());

# asList           : (TableHandle(c,b)) -> [c]
# insertrows       : (TableHandle(c,b), [b]) -> ()
# updaterows       : (TableHandle(c,b), [(c, b)]) -> ()
# deleterows       : (TableHandle(c,b), [c]) -> ()
# getDatabaseConfig : () -> (args:String,driver:String)

ignore(getDatabaseConfig());

# isAlpha          : (Char) -> Bool
# isAlnum          : (Char) -> Bool
# isLower          : (Char) -> Bool
# isUpper          : (Char) -> Bool
# isDigit          : (Char) -> Bool
# isXDigit         : (Char) -> Bool
# isBlank          : (Char) -> Bool
# toUpper          : (Char) -> Char

ignore(toUpper('1'));

# toLower          : (Char) -> Char

ignore(toLower('1'));

# ord              : (Char) -> Int

ignore(ord(' '));

# chr              : (Int) -> Char

ignore(chr(257));

# assert(ord(chr(257)) == true);

# floor            : (Float) -> Float

ignore(floor(17.0));

# ceiling          : (Float) -> Float

ignore(ceiling(17.0));

# cos              : (Float) -> Float

ignore(cos(17.0));

# sin              : (Float) -> Float

ignore(sin(17.0));

# tan              : (Float) -> Float

ignore(tan(17.0));

# log              : (Float) -> Float

ignore(log(17.0));

# sqrt             : (Float) -> Float

ignore(sqrt(49.0));

# ~                : (String, mu a . [|Any:()|Range:(Char, Char)|Repeat:([|Plus:()|Question:()|Star:()|], a)|Seq:[a]|Simply:String|]) -> Bool

# environment      : () -> [(String, String)]

# ignore(environment());      # Not implemented

# error            : (String) -> a

ignore(error("All tests completed!"));
}

{
  test();
  page <html><body>ok</body></html>
}
