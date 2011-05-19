#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config
# Normalisation by evaluation in Links
#
# This is an implementation of NBE for a sub-language of Links
# including: type variables, arrows, binary products, unit
# and records
#
# norm(t)(v)
#   takes
#    t, an encoding of a type
#    v, a value of the type encoded by t
# and returns the long beta-eta normal form of v
# ('long' in the sense that normal forms correspond to
# applying eta as a type-directed expansion)
#
# np is the same as norm, except it pretty prints
# the output as valid links code.

## utility functions
# foldr on lists
fun foldr(f) {fun (a) {fun (xs) {
   switch (xs) {
    case x::xs ->  f(x)(foldr(f)(a)(xs))
    case [] -> a
   }
}}}

# new line
fun nl() {"
"}

## name generation
# create a name supply process
var nameSupply = spawn {
 fun gen(count) {
  receive {
   case (Fresh(pid, prefix)) -> {
    var count = count+1;
    pid ! (prefix ++ (intToString(count)));
     gen(count)
   }
   case Reset -> {gen(0)}
  }
 }
 gen(0)
};

# return a fresh name with the specified prefix
fun getFreshName(prefix) {
 nameSupply ! Fresh(self(), "x");
 recv()
}

## nbe
# the algorithm is built up using reify / reflect pairs encoded
# in the types

# type variables a, b, c
# (exp -> exp, exp -> exp)
var a = (fun (v) {v}, fun (x) {x});
var b = a;
var c = a;

# arrow types (a -> b)
#
# ((a -> exp, exp -> a) * (b -> exp, exp -> b))
# ->
# ((a -> b) -> exp * exp -> (a -> b)) 
fun arrow((reifya, reflecta), (reifyb, reflectb)) {
 (fun (f) {
  var x = getFreshName("x");
   Lam(x, reifyb(f(reflecta(Var(x)))))
  },
  fun (e) {
   fun (v) {
    reflectb(App(e, reifya(v)))
   }
  }
 )
}

# product types (a * b)
#
# ((a -> exp, exp -> a) * (b -> exp, exp -> b))
# ->
# ((a * b) -> exp * exp -> (a * b)) 
fun product((reifya, reflecta), (reifyb, reflectb)) {
 (fun (v,w) {
   Pair(reifya(v), reifya(w))
   },
  fun (e) {
   (reflecta(ProjLeft(e)), reflectb(ProjRight(e)))
  }
 )
}

# note: we have no way of distinguishing the
# type of empty open records "(a)" with that of
# a raw type variable "a"
# (a) -> exp * exp -> (a)
var unit = (fun (x) {Unit}, fun (e) {()});

# reify0 : (name: a|b) -> String * Expression
# reflect0 : Expression * (b) -> (name: a|b)
fun extend((reify0, reflect0), (reify1, reflect1)) {
 (fun (r) {
   Extend(reify0(r), reify1(r))
  },
  fun (e) {
   reflect0(e, reflect1(e))
  }
 )
}

# embed : a * b -> (name: a|b)
# project : (name: a|b) -> a
# reify : a -> Expression
# reflect : Expression -> a
fun field(name, embed, project) {fun (reify, reflect) {
  (fun (r) {(name, reify(project(r)))},
   fun (e, s) {embed(reflect(Proj(name,e)), s)}
  )
}}

# because we don't have first class labels, each one has to be
# declared explicitly
var label1 = field("label1", fun (v, s) {(label1=v|s)}, fun (label1=v|s) {v});
var label2 = field("label2", fun (v, s) {(label2=v|s)}, fun (label2=v|s) {v});
var label3 = field("label3", fun (v, s) {(label3=v|s)}, fun (label3=v|s) {v});
var label4 = field("label4", fun (v, s) {(label4=v|s)}, fun (label4=v|s) {v});
var label5 = field("label5", fun (v, s) {(label5=v|s)}, fun (label5=v|s) {v});
var label6 = field("label6", fun (v, s) {(label6=v|s)}, fun (label6=v|s) {v});
var label7 = field("label7", fun (v, s) {(label7=v|s)}, fun (label7=v|s) {v});
var label8 = field("label8", fun (v, s) {(label8=v|s)}, fun (label8=v|s) {v});
var label9 = field("label9", fun (v, s) {(label9=v|s)}, fun (label9=v|s) {v});

var name = field("name", fun (v, s) {(name=v|s)}, fun (name=v|s) {v});
var age = field("age", fun (v, s) {(age=v|s)}, fun (age=v|s) {v});

# normalise a value as an expression
fun norm(reifyt, reflectt) {fun (v) {
  nameSupply ! Reset;
  reifyt(v)
}}

# pretty printer
fun expToString(exp) {
 fun indent(i) {
  if (i == 0) {""}
  else {" " ++ indent(i-1)}
 }
 fun ets(i) {fun (exp) {
   switch (exp) {
    case Var(s) -> s
    case Lam(x, m) -> {"fun (" ++ x ++ ") {" ++ nl() ++
	indent(i+1) ++ ets(i+1)(m) ++ nl() ++ indent(i) ++ "}"}
    case App(m, n) -> {ets(i)(m) ++ "(" ++ ets(i)(n) ++ ")"}
    case Unit -> "()"
    case Extend((name, m), n) -> {"(" ++ (name ++ "=" ++ ets(i)(m)) ++
	("," ++ ets(i)(n) ++ ")")}
    case Proj(name, m) -> {ets(i)(m) ++ "." ++ name}
    case Pair(m, n) -> {"(" ++ ets(i)(m) ++ "," ++ ets(i)(n) ++ ")"}
    case ProjLeft(m) -> {ets(i)(m) ++ ".1"}
    case ProjRight(m) -> {ets(i)(m) ++ ".2"}
   }
 }}
 ets(0)(exp)
}

# normalise and print a value
fun np(type)(value) {
 print(expToString(norm(type)(value)))
}

### Examples
## (not really very interesting yet)

np (arrow(a, a)) (fun (x) {x})
np (arrow(arrow(a, a), arrow(a, a))) (fun (x) {x})

var rname = extend(name(a), unit)
np (arrow(arrow(rname, rname), arrow(rname, rname))) (fun (x) {x})

var rnameage = extend(name(a), extend(age(b), unit))
np (arrow(product(a, b), rnameage)) (fun (x, y) {(name=x, age=y)})
np (arrow(rnameage, rnameage)) (fun (x) {x})
np (arrow(arrow(rnameage, rnameage), arrow(rnameage, rnameage))) (fun (x) {x})

# type of Church numerals
var numType = arrow(arrow(a, a), arrow(a, a));

# return the i-th Church numeral
fun num(i) {
 if (i == 0) {fun (f) {fun (x) {x}}}
 else {
  fun (f) {fun (x) {f(num(i-1)(f)(x))}}
 }
}

# compute the sum of two Church numerals
var plus = fun (m) {fun (n) {fun (f) {fun (x) {
    m(f)(n(f)(x))
}}}}


np (numType)(plus(num(8))(num(15)))
