#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun f(n) client {
  var n = n + 1 - 1;
  page
   <body>
     on client   
     <a l:href="{f(n+1)}">inc client {intToXml(n)}</a> <br />
     <a l:href="{g(n+1)}">inc server {intToXml(n)}</a>
   </body>
}

fun g(n) server {
  page
   <body>
     on server
     <a l:href="{f(n+1)}">inc client {intToXml(n)}</a> <br />
     <a l:href="{g(n+1)}">inc server {intToXml(n)}</a>
   </body>
}

f(0)

