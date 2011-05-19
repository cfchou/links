#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


fun showAttr(id, attr) client {
  switch elementById(id) {
   case Some s ->  switch attribute(s, attr) {
                     case Some s -> debug("show " ++ id ++ " : found an element whose " ++ attr ++ " attribute is " ++s);
                     case None   -> debug("show " ++ id ++ " : found an element, but no " ++ attr ++ " attribute");
                   };
   case None   ->  debug("show " ++ id ++ " : couldn't find an element");
  }   
}

<body>
<ul>
  <li id="foo" style="width: 120px">foo item</li>
  <li id="bar" style="width: 130px">bar item</li>
  <li id="baz">bar item</li>
</ul>
<a l:onclick="{showAttr("foo", "style")}">Show foo's style</a>
<a l:onclick="{showAttr("bar", "style")}">Show bar's style</a>
<a l:onclick="{showAttr("baz", "style")}">Show baz's style</a>
<a l:onclick="{showAttr("quuz", "style")}">Show quuz's style</a>
</body>
