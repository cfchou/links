#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


fun fst(x) { (a, b) = x; a }
fun snd(x) { (a, b) = x; b }

fun assoc(d, a, l) {
  if (l == []) d
  else if (a == hd(l).1)
    hd(l).2
  else assoc(d, a, tl(l));
}

table "dict" (
   word : String, 
   definition : String
) order [word:asc] database "postgresql:gcide:localhost:5432:s0567141:";

fun lookup_data(word) server {
  for (defn <- dict)
  where (defn.word == word)
    [defn.definition]
}

fun lookup(word) client {
  defn = lookup_data(word);
  for defn <- defn in
  <html>
     <h1>{enxml(word)}</h1>
    <div>
      {enxml(word ++ ": " ++ defn)}
    </div>
    <a l:onclick="{main([])}">Perform another lookup</a>
  </html>
}

fun main(suggestions) client {
  sugg_links = for suggestion <- suggestions in
    <a l:onclick="{lookup(suggestion)}">{enxml(suggestion)}</a><br />;
<html>
<body>
Look up a word's definition: <br />

<form method="POST" l:onsubmit="{lookup(word)}"
          l:onkeyup="{main(completions(word))}">
<input type="text" l:name="word" value="" />
<input type="submit" name="btn" value="Submit" />
</form>

<div id="results">
   {if (sugg_links == []) <br /> else 
     <div>Suggestions: <br /> {sugg_links}</div>
   }
</div>

</body>
</html>
}

# <a l:onclick="{lookup(suggestion)}">{enxml(suggestion)}</a>
# ;  if (x == []) "" else <div>Suggestions: <br /> {x}</div>

fun join(glue, lyst) {
  if (lyst == [])
    ""
  else
    hd(lyst) ++ glue ++ join(glue, tl(lyst));
#  ""
}

fun prefixof(p, str) {
  if (p == "") true
  else if (str == "") false
  else if (hd(p) == hd(str)) prefixof(tl(p), tl(str))
  else false
}

fun completions(p) server {
  if (p == "") [] else {
    results = for (w <- dict)
              where (w.word beginswith p)
              in [w.word];
    results
  }
}

main([])

