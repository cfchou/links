#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# A test of client stubs / server stubs called from the other side.
fun f() client {
  alertDialog(intToString(serverTime()))
}

fun g() server { 
  alertDialog("this is the server talking.")
}

page
  <html>
    <p><a href="#" l:onclick="{f()}">Call serverTime from the client</a></p>
    <a href="#" l:onclick="{g()}">Call alertDialog from the server</a>
  </html>
