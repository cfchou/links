#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
fun date() server {
  getCommandOutput("date")
}

fun showDate() client {
  replaceNode(
     <div id="date">{stringToXml(date())}</div>,
     getNodeById("date"))
      
}

fun ticker(f, n) {
  f();
  sleep(n);
  ticker(f, n);
}

fun (){
  spawn { ticker(showDate, 5) };
  <html>
    <body>
      <div id="date"/>
    </body>
  </html>
}
