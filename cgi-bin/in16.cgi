#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

#??
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];
typename Beh(a) = (Float){}~>a;

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

sig const : (a) -> Beh(a)
fun const(v) { fun (t:Float) { v } }

fun iAddB(iB, jB) { fun (t:Float) { iB(t) + jB(t) } }
fun iSubB(iB, jB) { fun (t:Float) { iB(t) - jB(t) } }
fun iMulB(iB, jB) { fun (t:Float) { iB(t) * jB(t) } }
fun iDivB(iB, jB) { fun (t:Float) { iB(t) / jB(t) } }

fun fAddB(iB, jB) { fun (t:Float) { iB(t) +. jB(t) } }
fun fSubB(iB, jB) { fun (t:Float) { iB(t) -. jB(t) } }
fun fMulB(iB, jB) { fun (t:Float) { iB(t) *. jB(t) } }
fun fDivB(iB, jB) { fun (t:Float) { iB(t) /. jB(t) } }

fun itofB(iB) { fun (t:Float) { intToFloat(iB(t)) } }

fun ftoiB(iB) { fun (t:Float) { floatToInt(iB(t)) } }

var time = fun (t:Float) { t };

fun fasterB(fB, xB) {
    fun (t:Float) {
        xB((time `fMulB` fB)(t))
    } 
}

fun slowerB(fB, xB) { 
    fun (t:Float) {
        xB((time `fDivB` fB)(t))
    } 
}

fun over(elm1B, elm2B) {
    fun (attr) {
        fun (t:Float) {
            <#>
            {elm2B(attr)(t)}
            {elm1B(attr)(t)}
            </#>
        }
    }
}

fun move(elmB, xB, yB) {
    fun (attr:(posX:Beh(Float), posY:Beh(Float) |_)) {
        fun (t:Float) {
            var new = (attr with posX = attr.posX `fAddB` xB,
                                 posY = attr.posY `fAddB` yB);

            elmB(new)(t)
        }
    }
}

fun stretch(elmB, wB, hB) {
    fun (attr:(width:Beh(Float), height:Beh(Float) |_)) {
        fun (t:Float) {
            var new = (attr with width = attr.width `fAddB` wB,
                                 height = attr.height `fAddB` hB);
            elmB(new)(t)
        } 
    }
}

fun pointToCoord(xB, yB) {
    fun (t:Float) {
        (xB(t), yB(t))
    }
}

fun rotateAbout(elmB, aB, coordB) {
    fun (attr) {
        fun (t:Float) {
            elmB((attr with roAngle = aB, roAbout = coordB))(t)
        } 
    }
}

fun rotate(elmB, aB) {
    fun (attr) {
        fun (t:Float) {
            elmB((attr with roAngle = aB))(t)
        } 
    }
}

fun withImg(elmB, pathB) {
    fun (attr:(hrefImg:Beh(String) |_)) {
        fun (t:Float) {
            elmB((attr with hrefImg = pathB))(t)
        }
    }
}

fun withColor(elmB, colorB) {
    fun (attr:(color:Beh(String) |_)) {
        fun (t:Float) {
            elmB((attr with color = colorB))(t)
        }
    }
}

fun rect(id) {
    fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
               height:Beh(Float), color:Beh(String),
               stroke:Beh(String), strokeWidth:Beh(Float),
               roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) {
        fun (t:Float) {
            var x = intToString(floatToInt(attr.posX(t)));
            var y = intToString(floatToInt(attr.posY(t)));
            var w = floatToInt(attr.width(t));
            var h = floatToInt(attr.height(t));
            var s = floatToInt(attr.strokeWidth(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <rect id="{id}"  
            transform="rotate({a}, {ri}, {rj})"
            x="{x}" 
            y="{y}"
            width="{intToString(w)}"
            height="{intToString(h)}"
            style="fill:{attr.color(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

fun ellipse(id) {
    fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
               height:Beh(Float), color:Beh(String),
               stroke:Beh(String), strokeWidth:Beh(Float),
               roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));
            var w = floatToInt(attr.width(t) /. 2.0);
            var h = floatToInt(attr.height(t) /. 2.0);
            var s = floatToInt(attr.strokeWidth(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <ellipse id="{id}"  
            transform="rotate({a}, {ri}, {rj})"
            cx="{intToString(x)}" 
            cy="{intToString(y)}"
            rx="{intToString(w)}"
            ry="{intToString(h)}"
            style="fill:{attr.color(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

fun image(id) {
    fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
               height:Beh(Float), hrefImg:Beh(String),
               roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));
            var w = floatToInt(attr.width(t));
            var h = floatToInt(attr.height(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <image id="{id}" 
            transform="rotate({a}, {ri}, {rj})"
            x="{intToString(x)}" 
            y="{intToString(y)}" 
            width="{intToString(w)}" 
            height="{intToString(h)}" 
            xlink:href="{attr.hrefImg(t)}"/>
        }
    }
}

fun svg(id, elmB, wB, hB) {
    fun (t:Float) {
        var sw = intToString(floatToInt(wB(t)));
        var sh = intToString(floatToInt(hB(t)));
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
        xmlns:xlink="http://www.w3.org/1999/xlink"
        id="{id}" width="{sw}" height="{sh}"
        viewbox="0 0 {sw} {sh}" >
        <#>
        {elmB((posX = const(0.0), posY = const(0.0), width = const(1.0),
               height = const(1.0), color = const("white"), 
               stroke = const("black"), strokeWidth = const(5.0),
               hrefImg = const(""),
               roAngle = const(0.0), roAbout = const((0.0, 0.0))))(t)}
        </#>
        </svg>
    }
}

# [COMPOSE] ==========================================
var wiggleA = sin;
var waggleA = cos;

var pWiggleA = const(1.0) `fAddB` wiggleA;
var pWaggleA = const(1.0) `fAddB` waggleA;

fun compose() {
    #-- image1
    var w = (const(80.0) `fMulB` pWiggleA) `fAddB` const(80.0);
    var h = (const(60.0) `fMulB` pWiggleA) `fAddB` const(60.0);
    var luigi = const("photos_files/Paperluigi.png");

    var m1 = stretch(move(image("m1") `withImg` luigi,
                            const(400.0), const(100.0)),
                slowerB(const(300.0), w),
                slowerB(const(300.0), h));

    #-- image2 revolve
    var x = (const(200.0) `fMulB` pWiggleA) `fAddB` const(50.0);
    var y = (const(200.0) `fMulB` pWaggleA) `fAddB` const(50.0);
    var mario = const("photos_files/super_mario_theme.png");

    var m2 = stretch(move(image("m2"),
                            slowerB(const(1500.0), x),
                            slowerB(const(500.0), y)),
                const(100.0), const(100.0)) `withImg` mario;
    
    #-- circle
    var chubby = (const(60.0) `fMulB` wiggleA) `fAddB` const(40.0);
    var chubby2 = slowerB(const(500.0), chubby);
    var d1 = move(ellipse("d1"), const(100.0), const(100.0)); 
    var d2 = stretch(d1, chubby2, chubby2) `withColor` const("red");

    #-- rectangle
    var r1 = stretch(move(rect("r1"), const(100.0), const(100.0)),
                    chubby2, chubby2);
    var r2 = rotateAbout(r1, const(45.0), const((100.0, 100.0)));

    svg("svg1",
        d2 `over` r2 `over` m1 `over` m2,
        const(800.0), const(600.0))
}


# [WEB] ==========================================

fun drawImage1(scene, t0, tEnd) client {
    if (not (pressed("drawImage1"))) {
        var svgXml = scene(intToFloat(clientTime()));

        var name = getAttribute(svgXml, "id");
        if (isNull(getNodeById(name))) {
            appendChildren(svgXml, getNodeById("svgbasics"));
        } else {
            replaceNode(svgXml, getNodeById(name)); 
        };
        doDrawImage(scene, t0, tEnd);
    } else {
            removeNode(getNodeById("svg1"));
    }
}

fun doDrawImage(scene, t0, tEnd) client {
    var now = clientTime();
    if (now < tEnd) {
            var svgXml = scene(intToFloat(now));

            var name = getAttribute(svgXml, "id");
            replaceNode(svgXml, getNodeById(name)); 
            
            doDrawImage(scene, t0, tEnd);
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
        
var scene = compose();

page
<html>
<head>
<style>
    #svgbasics {{ width: 800px; height: 600px; border: 1px solid #484; }}
</style>
</head>

<body>
<button id="press1" type="button" l:onclick="{var t = clientTime(); ignore(spawn { drawImage1(scene, t, t + 10000)}) }">
    draw image1</button>

<div id="svgbasics">
</div>
</body>
 </html>
