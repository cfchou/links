#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun firstButton(plus,times) {
   if(plus) {(+)}
   else if(times) {(*)}
   else {error("unknown button")}
}

var f = 
  formlet 
   <#>
     {inputInt -> l}
     {inputInt -> r}
     <br/>
     {submitButton("+") -> plus}
     {submitButton("*") -> times}
   </#>
  yields (action=firstButton(plus,times), l=l,r=r);

fun run ((action=action, l=l, r=r)) {
  page
   <html>
    <body>
     {intToXml(l `action` r)}
    </body>
   </html>
}

page
 <html>
  <body>
   {f => run}
  </body>
 </html>

