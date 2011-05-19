#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
var num=200000;

fun pass_it_on(pid) {
  pid ! recv()+1;
}

fun create_processes(n, prevpid) {
  if (n == 0) spawn { pass_it_on(prevpid) }
  else {
   if (mod(n)(1000) == 0) print(".") else ();
   var thispid = spawn { pass_it_on(prevpid) };
   create_processes(n - 1, thispid)
  }
}

fun run()
{
  var input = 42;
  print("Spawning " ++ intToString(num) ++ " server processes.
Input is: "++intToString(input));
  var last_pid = create_processes(num, self());
  last_pid ! input;
  print("Done. Output is: "++intToString(recv())++" isn't this ");
  run
}

run()
