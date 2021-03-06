#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun lowercase(s) {
  implode(for (c <- explode(s)) [toLower(c)])
}

fun suggest(pre) client {
 replaceChildren(
  format(completions(lowercase(pre))),
  getNodeById("suggestions") 
 )
} 

fun format(words) {
 for (w <- words)
  <span>
   <b>{stringToXml(w.word)}</b>
   <i>{stringToXml(w.type)}</i>:
      {stringToXml(w.meaning)}
   <br/>
  </span>
}

fun completions(pre) server {
 var wordlist = table "wordlist" with (
   word : String, 
   type : String, 
   meaning : String
 ) from (database "dictionary");

 if (pre == "") []
 else {
  query [10] {
   for (w <-- wordlist)
    where (w.word =~ /^{pre}.*/)
    orderby (w.word)
     [w]
  }
 }
}

fun main() {
  var handler = spawn {
   fun receiver() {
    receive { case Suggest(pre) -> suggest(pre); receiver() }
   }
   receiver()
  };

  page
   <html>
    <head>
     <title>Dictionary suggest</title>
    </head>
    <body>
     <h1>Dictionary suggest</h1>
     <form l:onkeyup="{handler!Suggest(pre)}">
      <input type="text" l:name="pre"
             autocomplete="off"/>
     </form>
     <div id="suggestions"/>
    </body>
   </html>
}

main()

