#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


fun thanks(name) {
    <html>
      Thanks for logging in, {enxml(name)}.
    </html>
}

fun login_widget(msg) {
        <html>
          {enxml(msg)}
          <form l:action="{validate(username, userpass)}" method="post">
            <table>
              <tr>
	        <td>Username:</td>
                <td> <input l:name="username" value="" /></td>
              </tr>
              <tr>
                <td>Password:</td>
                <td><input type="password" l:name="userpass" value="" /></td>
	      </tr>
            </table>
            <input type="submit" />
          </form>
	  <a href="test4.cgi">start again</a>
        </html>
}

fun validate(name, pass) {
  if (name == "ezra" && pass == "knock")
    thanks(name)
  else
    login_widget("wrong")
}

login_widget("Please log in below:")
