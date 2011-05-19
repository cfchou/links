#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
var db = database "todo";
var items = table "items" with (name : String) from db;

fun showList() server {
 page
  <html>
   <body>
    <form l:action="{add(item)}" method="POST">
      <input l:name="item"/>
      <button type="submit">Add item</button>
    </form>
    <table>
     {for (item <- query {for (item <-- items) [item]})
        <tr><td>{stringToXml(item.name)}</td>
            <td><form l:action="{remove(item.name)}" method="POST">
                 <button type="submit">Done</button>
                </form>
            </td>
        </tr>}
     </table>
    </body>
  </html>
}

fun add(name) server {
 insert items values [(name=name)];
 showList()
}

fun remove(name) server {
 delete (r <-- items) where (r.name == name);
 showList()
}

showList()
