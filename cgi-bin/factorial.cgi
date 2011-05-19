#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun request(s) client {
  <html>
   <body>
    <h1>Please type a number</h1>
     <form l:onsubmit="{response(t)}" l:onkeyup="{replaceDocument(request(t))}">
      <input type="text" value="{s}" l:name="t"/>
      {
      if (s =~ /^[0-9]+/)
       <input type="submit"/>
      else
       <input type="submit" disabled="disabled"/>
      }
     </form>
    </body>
  </html>
}

fun response(s) client {
 var n = stringToInt(s);

 replaceDocument(
  <html>
   <body>
    <h1>Factorials up to {intToXml(n)}</h1>
    <table><tbody>{
     for ((i=i,f=f) <- lookupFactorials(n))
      <tr>
       <td>{intToXml(i)}</td>
       <td>{intToXml(f)}</td>
      </tr>
    }</tbody></table>
   </body>
  </html>
 )
}

fun lookupFactorials(n) server {
 var db = database "factorials";
 var factorials = table "factorials" with (i : Int, f : Int) from db;

 query {
   for (row <-- factorials)
    where (row.i <= n)
    orderby (row.i)
     [(i=row.i, f=row.f)]
 }
}

page
  <#>{request("")}</#>
