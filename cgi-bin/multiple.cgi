#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun enterNumbers(n) {
  page
   <html>
     <h1>Enter {intToXml(n)} numbers:</h1>
     {withSubmit(formlets(replicate(n, inputInt))) =>
        fun (xs) {page <html><body>{intToXml(sum(xs))}</body></html>}}
   </html> 
}

fun withSubmit(f) {
  formlet
    <#>{f -> v}{submit("Submit")}</#>
  yields
    v
}

page
 <html>
    <h1>Multiple</h1>
    Enter numbers: {withSubmit(inputInt) => enterNumbers}
 </html>
