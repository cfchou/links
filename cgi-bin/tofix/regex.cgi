#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun f(number) client {
  domAppendChild(
     <p>{stringToXml(number ++ (if (number ~ /[0-9]+/) " is a number" 
                          else " is a non-number"))}</p>,
     getNodeById("div"))
}

<html>
   <body>
     <h1>Enter a string</h1>
     <form l:onsubmit="{f(number)}">
      <input l:name="number"/>
      <input type="submit" value="Submit"/>
     </form>
     <div id="div"/>
   </body>
</html>
