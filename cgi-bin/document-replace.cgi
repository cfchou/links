#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun change() client {
  replaceDocument(
   <html>
    <body> 
       new page
    </body>
   </html>
  )
}

page
 <html>
 <body>
 <a l:onclick="{change()}">change</a>
 </body>
 </html>
