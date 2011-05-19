#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
typename Channel (a) = ((() {}~> a), ((a) {}~> ()));

sig newChannel : () ~> Channel (a)
fun newChannel() {
  var p =
    spawn {
      fun step(vs, readers) {
        receive {
          case Value(v) ->
            var (v :: vs) = vs ++ [v];
            switch (readers) {
              case [] -> step (v :: vs, readers)
              case (r :: readers) -> r ! v; step (vs, readers)
            }
          case Read(r) ->
            var (r :: readers) = readers ++ [r];
            switch (vs) {
              case [] -> step (vs, r :: readers)
              case (v :: vs) -> r ! v; step (vs, readers)
            }
        }
      }
      step([], [])
    };

  fun write(v) {
    p ! Value(v)
  }

  fun read() {
    spawnWait {
      p ! Read(self());
      receive { case v -> v }
    }
  }

  (read, write)
}

sig get : (Channel (a)) ~e~> a
fun get ((read, _)) { (read : () ~e~> a <- () {}~> (a))() }

sig put : (Channel (a), a) ~e~> ()
fun put((_, write), v) { (write : (a) ~e~> () <- (a) {}~> ())(v) }
