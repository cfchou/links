#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# Spawn a ring of n processes.
# Pass an integer around the ring, incrementing it each time it passes
# through a process.  Print out the result when it gets back to main.

var num=150;

fun append(xml) {
  var progress = domGetRefById("progress");
  domAppendChild(xml, progress)
}

fun f(pid) client {
  receive {
    case Message(n) -> {
        append(stringToXml(". "));
        pid ! Message(n+1)
    }
  }
}

fun myspawn(pid, n) {
  if (n == 0) pid
  else myspawn(spawn { f(pid) }, n-1)
}

fun run(input) client {
  append(stringToXml("Input is: "++input));
  var pid = myspawn(self(), num); ();
  pid ! Message (stringToInt(input));
  receive {
    case Message(n) -> {
        append(stringToXml(" Done. Output is: "++intToString(n)));
	append(<br />)
    }
  }
}

<html>
<body>
 <H1>Run {intToXml(num)} client processes</H1>
 <form l:onsubmit="{run(n)}">
   <input type="text" value="42" l:name="n" />
   <input type="submit" value="Run" />
 </form>
 <div id="progress">
 </div>
</body>
</html>
