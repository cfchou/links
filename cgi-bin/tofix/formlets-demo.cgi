#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# formlets in terms of idioms

# The naming idiom
typename Name (a) = (Int) {}~> (a,Int);

var name = (
  pure  = fun (v) (s) { (v,s) },
  apply = fun (f) (v) (s) { 
            var (f,s) = f(s);
            var (v,s) = v(s);
              (f(v), s)
          },
  fresh = fun (s) { ("input_" ++ intToString(s), s+1) }
) : (
  pure : (a) -> Name (a),
  apply : (Name ((a) ~> b)) -> (Name (a)) -> Name (b),
  fresh : Name (String)
);

# The environment idiom
typename Reader (a) = (Env) {}~> a;

var env = (
  pure  = fun (v) (_) { v },
  apply = fun (f) (v) (e) { f(e)(v(e)) },
  read  = fun (e) { e }
) : (
  pure  : (a) -> Reader (a),
  apply : (Reader ((a) ~> b)) -> (Reader (a)) -> Reader (b),
  read  : Reader (Env)
);

# The XML accumulation idiom
typename Accum (a) = (Xml, a);

var acc = (
  pure  = fun (v) { (<#/>, v) },
  apply = fun ((fx,f)) ((vx,v)) { (fx ++ vx, f(v)) },
  plug  = fun (xc) ((x,a)) { (xc(x),a) }

) : (
  pure  : (a) -> Accum (a),
  apply : (Accum ((a) ~> b)) -> (Accum (a)) ~?~> Accum (b),
  plug  : (XmlContext) -> (Accum(a)) {}~> Accum(a)
);

# The formlet idiom
typename Form (a) = Name (Accum (Reader (a)));

var form = (
  pure  = name.pure `compose` acc.pure `compose` env.pure,

  # NB: we can't define the composition operation as a function
  #     because we lose polymorphism of the arguments under HM
  apply = fun (f) { name.apply
                     (name.apply
                       (name.pure (fun (f) { acc.apply
                                              (acc.apply
                                                (acc.pure
                                                   (env.apply))(f))})) (f)) },
  plug  = name.apply `compose` name.pure `compose` acc.plug
) : (
  pure  : (a) -> Form (a),
  apply : (Form ((a) ~> b)) -> (Form (a)) ~?~> Form (b),
  plug  : (XmlContext) -> (Form (a)) -> Form(a)
);
