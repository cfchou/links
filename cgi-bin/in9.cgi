#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

typename Time = Int;
#??
#typename IntB() = ((Int) -> Int);
#typename Behaviour (a) = (Time) -> a;



# [API] =====================================
var id=1;
fun lastId () {
    id + 1
}

fun lift0(a) {
    fun(t) {
        a
    }
}

fun createSvg(w, h) {
        "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" 
        id=\"svg1\" width=\"800px\" height=\"300px\"
        viewbox=\"0 0 800 300\"> </svg>"
}

fun createCircle(x, y, r) {
    var id = "c" ^^ intToString(lastId()); 
    "<circle xmlns=\"http://www.w3.org/2000/svg\" id=\"" ^^ id ^^
    "\" cx=\"" ^^ intToString(x) ^^ "\" cy=\"" ^^ intToString(y) ^^
    "\" r=\"" ^^ intToString(r) ^^
    "\"style=\"fill:red; stroke:black; stroke-width:5\"> </circle>"
}

fun moveCircle(xB, yB, circleB) {
   fun (t) {
       var cirChar = explode(circleB(t));
       var x = xB(t);
       var y = yB(t);
       var (prevx, restx) = split('c', 'x', '=', cirChar);
       var rest = dropWhile (fun(c) {c <> ' '}, restx);

       var updated = prevx ++ ['c', 'x', '=', '\"'] ++ 
                     explode(intToString(x)) ++ ('\"'::rest);

       var (prevy, resty) = split('c', 'y', '=', updated);
       var rest2 = dropWhile (fun(c) {c <> ' '}, resty);
       implode(prevy ++ ['c', 'y', '=', '\"'] ++ explode(intToString(y)) 
           ++ ('\"'::rest2))
   }
}

fun contain(parentB, childB) {
    fun (t) {
        var paChars = explode(parentB(t));
        var chStr = childB(t);
        var tag = implode(takeWhile (fun(c) {c <> '>'}, paChars));
        var rest = implode(tl(dropWhile (fun(c) {c <> '>'}, paChars)));
        tag ^^ "> " ^^ chStr ^^ rest
    }
}

# [FIX] =====================================
fun split (x, y, z, ary) {
    rsplit(x, y, z, [], ary)
}

fun rsplit (x, y, z, prev, rest) {
    switch (rest) {
        case ([]) -> (prev ++ rest, [])
        case (_::[]) -> (prev ++ rest, [])
        case (_::_::[]) -> (prev ++ rest, [])
        case (a::b::c::xs) -> if (a == x && b == y && c == z) {
                               (prev, xs)
                           } else {
                               rsplit(x, y, z, prev ++ (a::b::c::[]), xs) 
                           }
    }
}

# ??
#sig foo2 : (Int, (Int) -> Int) -> ((Int) -> Int)
fun foo2(a, f) {
    fun(t) {
        var b = f(a);
        b
    }
}

# [COMPOSE] =====================================

fun compose() {
    var svgB = lift0(createSvg(800, 600));
    var cirB = lift0(createCircle(50, 100, 50));

    # need to overload (*) and other arithmetic operators for behaviours
    var xB = fun (t) { 50 + 5 * t };

    var yB = lift0(100);

    var cirMovingB = moveCircle(xB, yB, cirB);
    svgB `contain` cirMovingB
}

fun compose2() {
    var svgB = lift0(createSvg(800, 600));
    var cirB = lift0(createCircle(50, 100, 50));
    var cir2B = lift0(createCircle(500, 100, 50));

    var xB = fun (t) { 50 + 5 * t };
    var x2B = fun (t) { var cx = 500 - 5 * t;
                        if (cx > 50)
                            cx
                        else
                            50
                      };

    var yB = lift0(100);

    var cirMovingB = moveCircle(xB, yB, cirB);
    var cirMoving2B = moveCircle(x2B, yB, cir2B);
    (svgB `contain` cirMovingB) `contain` cirMoving2B
}

# [WEB] ==========================================

fun drawImage1(t0, t1) client {
    if (not (pressed("drawImage1"))) {
        var svgB = compose();
        var svgBXml = parseXml(svgB(0));

        appendChildren(svgBXml, getNodeById("svgbasics"));
        doDrawImage1(t0, t1);
    } else {
            removeNode(getNodeById("svg1"));
    }
}

fun doDrawImage1(t0, nFrame) client {
    var stepT = 200;    # millisecond
    var durT = 10000;   # duration
    var maxFrame = durT / stepT;

    var last = t0 + nFrame * stepT;
    var now = clientTime();

    if ((last - t0) < durT) {
        if ((now - last) < stepT) {
            sleep(stepT);   # give way
            doDrawImage1(t0, nFrame);
        } else {
                if (nFrame < maxFrame) {
                    var svgB = compose();
                    var svgBXml = parseXml(svgB(nFrame));

                    var name = getAttribute(svgBXml, "id");
                    replaceNode(svgBXml, getNodeById(name)); 
                    
                    doDrawImage1(t0, nFrame + 1);
                } else { 
                }
        }
    } else {
        #error(intToString(now) ^^ ":" ^^ intToString(t0));
    }
}


fun pressed(s) client {
    if (s == getCookie(s)) {
        setCookie(s, "");
        true
    } else {
        setCookie(s, s);
        false
    }
}
        

page
<html>
<head>
<style>
    #svgbasics {{ width: 800px; height: 300px; border: 1px solid #484; }}
</style>
</head>

<body>
<button id="press1" type="button" l:onclick="{drawImage1(clientTime(), 0)}">
    draw image1</button>

<div id="svgbasics">
</div>
</body>
 </html>
