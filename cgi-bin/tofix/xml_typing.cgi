#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
type Html = <html>{(<head>{Head}</head>)?}<body>{Body}</body></html>;;

type Head = (<title>{Latin1*}</title>)*;;

type Body = (<div>{Body}</div>|<p>{Text}</p>|<h1>{Text}</h1>|<ul>{(<li>{Body}</li>)*}</ul>)*;;

type Text = (Latin1*|<span>{Text}</span>|<a href>{Text}</a>|<a name>{Text}</a>)*;;

fun ul(list : [Body]) {
  fun make_list(list : [Body]) {
    (switch (list) {
        case [] -> <li></li>
        case head :: tail -> <li>{head}</li> @ make_list(tail)
      }) : ((<li>{Body}</li>)* <li></li>)
  }
  <ul>{make_list(list)}</ul>
};;

fun make_page(title, body : Body) {
  <html><head><title></title></head><body>{body}</body></html> : Html
};;
