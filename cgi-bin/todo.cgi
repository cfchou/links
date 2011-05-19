#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun remove(item, items) {
  switch (items) {
     case []    -> []
     case x::xs -> if (item == x) xs
                   else x::remove(item, xs)
  }
}


fun todo(items) client {
   <html>
    <body>
     <form l:onsubmit="{replaceDocument(todo(item::items))}">
       <input l:name="item"/>
       <button type="submit">Add item</button>
     </form>
     <table>
      {for (item <- items)
        <tr><td>{stringToXml(item)}</td>
            <td><form l:onsubmit="{replaceDocument(todo(remove(item,items)))}">
                 <button type="submit">Completed</button>
                </form>
            </td>
        </tr>}
      </table>
     </body>
   </html>
}

page
 <#>{todo(["add items to todo list"])}</#>
