#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
var charfuns = [("isAlpha", isAlpha),
                ("isAlnum", isAlnum),
                ("isLower", isLower),
                ("isUpper", isUpper),
                ("isDigit", isDigit),
                ("isXDigit", isXDigit),
                ("isBlank", isBlank)];

var mathfuns = [ ("floor", floor),
                 ("ceiling", ceiling),
                 ("cos", cos),
                 ("sin", sin),
                 ("tan", tan),
                 ("log", log),
                 ("sqrt", sqrt)];

fun msg(div, txt) {
   appendChildren(<#><span>{stringToXml(txt)}</span><br/></#>, div);
}

fun stringToFloat(s) { intToFloat(stringToInt(s)) }

fun go(c::rest) client {
  var div = getNodeById("stuff");
  for ((name, f) <- charfuns) {
    if (f(c)) msg(div, name ++ " " ++ [c] ++ " : true")
    else msg(div, name ++ " " ++ [c] ++ " : false");
    []
  };
  msg(div, "ord " ++ [c] ++ " " ++ intToString(ord(c)));
  msg(div, "chr.ord " ++ [c] ++ " " ++ [(chr(ord(c)))]);
  for ((name, f) <- mathfuns) {
      msg(div, name ++ " " ++ c::rest ++ " " ++ floatToString(f(stringToFloat(c::rest))));
      []
  }
;
}

page
 <html>
   <form l:onsubmit="{go(value)}">  <input l:name="value" value=""/>
   <input type="submit"/>
   </form>
   <div id="stuff"/>
 </html>
