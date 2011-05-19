#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


fun f() client { }

fun add() {
  dom ! AppendChild(id="foo", replacement=<p>stuff</p>)
}


<html>
<body id="foo">
<a l:onclick="{add()}">add</a>
</body>
</html>
