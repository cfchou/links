#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun intForm(label) {
  (f=formlet
       <#><b>{stringToXml(label)}</b>: {inputInt -> i}{submit("submit integer")}</#>
     yields
       i,
   h=fun (i) {
       page
        <html>
         <head><title>Page test</title></head>
         <body>
          For '{stringToXml(label)}' you entered the integer '{intToXml(i)}'.
         </body>
        </html>
   }
  )
}

var x = intForm("x");
var y = intForm("y");

page
 <html>
  <head><title>Page test</title></head>
  <body>
   {x.f => x.h}
   {y.f => y.h}
  </body>
 </html>
