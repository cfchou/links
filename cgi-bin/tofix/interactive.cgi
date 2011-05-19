#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];

fun member(elem, lyst) {
  if (lyst == []) false else
  if (elem == hd(lyst))
    true
  else member(elem, tl(lyst));
}
fun isdigit(word) {
  member(word, digits)
}
fun idx(elem, lyst) {
  if (lyst == []) -1 else
  if (elem == hd(lyst))
    0
  else 1 + idx(elem, tl(lyst));
}
fun isgreater(num, word) {
  num <> "" && (int_of_string(num) >> idx(word, digits))
}
fun ok(word,num) {
  isdigit(word) && isgreater(num,word)
}
fun nextpage (word, digit) {
  <html><body><h1>You typed {enxml(word)}, {enxml(digit)}</h1></body></html>
}
fun page (word, num) {
  <html><body><h1>Test page</h1>
  <form l:action="{ if (ok(word1,num1))
                        nextpage(word1,num1)
                    else page(word1,num1) }"
        method="POST">
     <input l:name="word1" type="text" value="{word}"/>
     <b>Type a digit as a word</b>
     { if (word == "") <font/>
       else if (isdigit(word)) <font color="blue">ok</font>
       else <font color="red">error: {word} is not a digit as a word!</font> }
     <br/>
     <input l:name="num1" value="{num}"/>
     <b>Type a number greater than the digit</b>
     { if (num == "" || not(isdigit(word))) <font/>
       else if (isgreater(num, word)) <font color="blue">ok</font>
       else <font color="red">error: {num} is not greater than {word}!</font> }
     <br/>
     { if (javascript && not(ok(word,num)))
             <input type="submit" value="submit" disabled="disabled"/>
        else <input type="submit" value="submit"/> }
     <br/>

  </form>
  </body></html>
}
page("", "") 
 
