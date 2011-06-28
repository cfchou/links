#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

#??
#typename IntB() = ((Int) -> Int);
#typename Behaviour (a) = (Time) -> a;
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];
typename Beh(a) = (Int){}~>a;

# ?? contains(elm1B, elm2B) 

# ??
#sig foo2 : (Int, (Int) -> Int) -> ((Int) -> Int)
fun foo2(a, f) {
    fun(t) {
        var b = f(a);
        b
    }
}

# [API] =====================================
fun newId () {
    var id = getCookie("lastId");
    if ("" == id) {
        setCookie("lastId", "1");
        "1"
    } else {
        var newid = intToString(stringToInt(id) + 1);
        setCookie("lastId", newid);
        newid
    }
}


# ===================================================================
#fun test((xxB:((Int) -> Int), yyB:((Int) -> Int))) {
#    fun (t) {
#        xxB(t);
#        yyB(t)
#    }
#}


sig const : (a) -> Beh(a)
fun const(v) { fun (t:Int) { v } }

fun iAddB(iB, jB) { fun (t:Int) { iB(t) + jB(t) } }
fun iSubB(iB, jB) { fun (t:Int) { iB(t) - jB(t) } }
fun iMulB(iB, jB) { fun (t:Int) { iB(t) * jB(t) } }
fun iDivB(iB, jB) { fun (t:Int) { iB(t) / jB(t) } }

fun fAddB(iB, jB) { fun (t:Int) { iB(t) +. jB(t) } }
fun fSubB(iB, jB) { fun (t:Int) { iB(t) -. jB(t) } }
fun fMulB(iB, jB) { fun (t:Int) { iB(t) *. jB(t) } }
fun fDivB(iB, jB) { fun (t:Int) { iB(t) /. jB(t) } }

fun itofB(iB) { fun (t:Int) { intToFloat(iB(t)) } }

fun ftoiB(iB) { fun (t:Int) { floatToInt(iB(t)) } }

var time = fun (t:Int) { t };

fun fasterB(fB, xB) {
    fun (t:Int) {
        xB(ftoiB((itofB(time) `fMulB` fB))(t))
    } 
}

fun slowerB(fB, xB) { 
    fun (t:Int) {
        xB(ftoiB((itofB(time) `fDivB` fB))(t))
    } 
}

fun moveA(elmB, xB, yB) {
    fun (xB2, yB2, wB, hB) {
        fun (t:Int) {
            elmB(xB `iAddB` xB2, yB `iAddB` yB2, wB, hB)(t)
        }
    }
}

#fun resizeA(elmB, wB, hB) {
#    fun (xB, yB, _, _) {
#        fun (t:Int) {
#            elmB(xB, yB, wB, hB)(t)
#        } 
#    }
#}

fun stretchA(elmB, wFB, hFB) {
    fun (xB, yB, wB, hB) {
        fun (t:Int) {
            elmB(xB, yB, 
                ftoiB(itofB(wB) `fMulB` wFB),
                ftoiB(itofB(hB) `fMulB` hFB))(t)
        } 
    }
}

fun combineA(elm1B, elm2B) {
    fun (xB, yB, wB, hB) {
        fun (t:Int) {
            <#>
            {elm1B(xB, yB, wB, hB)(t)}
            {elm2B(xB, yB, wB, hB)(t)}
            </#>
        }
    }
}

fun circleA(id) {
    #(a:(Int) -> Int,b:Int)
    #fun ((xB:((Int) -> Int), yB:((Int) -> Int), wB:((Int) -> Int), 
    #    hB:((Int) -> Int))) 
    fun (xB, yB, wB, hB) {
        fun (t:Int) {
            var h = hB(t) / 2;
            var w = wB(t) / 2;
            if (w == h) {
                <circle id="{id}" 
                cx="{intToString(xB(t))}" 
                cy="{intToString(yB(t))}"
                r="{intToString(w)}"
                style="fill:red; stroke:black; stroke-width:5" />
            } else {
                <ellipse id="{id}"  
                cx="{intToString(xB(t))}" 
                cy="{intToString(yB(t))}"
                rx="{intToString(w)}"
                ry="{intToString(h)}"
                style="fill:red; stroke:black; stroke-width:5" />
            }
        }
    }
}

fun imageA(id, path) {
    fun (xB, yB, wB, hB) {
        fun (t:Int) {
            <image id="{id}" 
            x="{intToString(xB(t))}" 
            y="{intToString(yB(t))}" 
            width="{intToString(wB(t))}" 
            height="{intToString(hB(t))}" 
            xlink:href="{path}"/>
        }
    }
}

fun svgA (id, elmB, wB, hB) {
    fun (t:Int) {
        var sw = intToString(wB(t));
        var sh = intToString(hB(t));
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
        xmlns:xlink="http://www.w3.org/1999/xlink"
        id="{id}" width="{sw}" height="{sh}"
        viewbox="0 0 {sw} {sh}" >

        <#>
        {elmB(const(0), const(0), const(1), const(1))(t)}
        </#>
        </svg>
    }
}

# [COMPOSE] ==========================================

#var wiggleA = fun (t:Int) {
#                  var tt = floatToInt(intToFloat(t) /. 500.0);
#                  sin(intToFloat(tt))
#              };
#var waggleA = fun (t:Int) {
#                  var tt = floatToInt(intToFloat(t) /. 500.0);
#                  cos(intToFloat(tt))
#              };

# [FIX]
var wiggleA2 = fun (t:Int) { sin(intToFloat(t) /. 500.0) };
var waggleA2 = fun (t:Int) { cos(intToFloat(t) /. 500.0) };
var pWiggleA2 = const(1.0) `fAddB` wiggleA2;
var pWaggleA2 = const(1.0) `fAddB` waggleA2;


var wiggleA = fun (t:Int) { sin(intToFloat(t)) };
var waggleA = fun (t:Int) { cos(intToFloat(t)) };

var pWiggleA = const(1.0) `fAddB` wiggleA;
var pWaggleA = const(1.0) `fAddB` waggleA;

fun compose() {
    #-- image1
    var w = (const(80.0) `fMulB` pWiggleA) `fAddB` const(80.0);
    var h = (const(60.0) `fMulB` pWiggleA) `fAddB` const(60.0);

    var m1 = stretchA(moveA(imageA("m1", "photos_files/Paperluigi.png"),
                const(500), const(100)),
                slowerB(const(200.0), w),
                slowerB(const(200.0), h));

    #-- image2
    var x = (const(200.0) `fMulB` pWiggleA) `fAddB` const(50.0);
    var y = (const(200.0) `fMulB` pWaggleA) `fAddB` const(50.0);

    var m2 = stretchA(moveA(imageA("m2",
                "photos_files/super_mario_theme.png"),
                slowerB(const(200.0), ftoiB(x)),
                slowerB(const(200.0), ftoiB(y))),
                const(100.0), const(100.0));
    
    #-- image3 (smoother)
    var x = (const(200.0) `fMulB` pWiggleA2) `fAddB` const(50.0);
    var y = (const(200.0) `fMulB` pWaggleA2) `fAddB` const(50.0);
    var m3 = stretchA(moveA(imageA("m3",
                "photos_files/Paperluigi.png"),
                ftoiB(x), ftoiB(y)),
                const(100.0), const(100.0));

    #-- circle
    var chubby = (const(60.0) `fMulB` wiggleA) `fAddB` const(40.0);
    var chubby2 = slowerB(const(200.0), chubby);
    var d1 = moveA(circleA("d1"), const(100), const(100)); 
    var d2 = stretchA(d1, chubby2, chubby2);

    svgA("svg1",
        d2 `combineA` m1 `combineA` m2 `combineA` m3,
        const(800), const(600))
}


# [WEB] ==========================================

fun drawImage1(t0, tEnd) client {
    if (not (pressed("drawImage1"))) {
        var svgXml = compose()(0);
        appendChildren(svgXml, getNodeById("svgbasics"));
        doDrawImage(t0, tEnd);
    } else {
            removeNode(getNodeById("svg1"));
    }
}

fun doDrawImage(t0, tEnd) client {
    var now = clientTime();
    if (now < tEnd) {
            var svgXml = compose()(now);

            var name = getAttribute(svgXml, "id");
            replaceNode(svgXml, getNodeById(name)); 
            
            doDrawImage(t0, tEnd);
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
    #svgbasics {{ width: 800px; height: 600px; border: 1px solid #484; }}
</style>
</head>

<body>
<button id="press1" type="button" l:onclick="{var t = clientTime(); ignore(spawn { drawImage1(t, t + 10000)}) }">
    draw image1</button>

<div id="svgbasics">
</div>
</body>
 </html>
