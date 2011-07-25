#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

#??
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];
typename Time = Float;
typename Beh(a) = (Time){}~>a;

typename FPair = (Float, Float);
typename Points = [FPair];

typename Attrs = (posX:Beh(Float), posY:Beh(Float),
                  height:Beh(Float), width:Beh(Float),
                  fill:Beh(String), hrefImg:Beh (String),
                  stroke:Beh(String), strokeWidth:Beh(Float),
                  roAbout:Beh((Float, Float)), roAngle:Beh(Float),
                  points:Beh(Points),
                  text:Beh(String),
                  ffamily:Beh(String), fsize:Beh(Float),
                  fweight:Beh(String));

#typename Shape = (Attrs){}~> (Float){}~> Xml;
typename SBeh = (Attrs){}~> Beh(Xml);

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

fun fst((a, _)) { a }
fun snd((_, b)) { b }

sig fstB : (Beh((a, a))) -> Beh(a)
fun fstB(cB) { fun (t:Float) { fst(cB(t)) } }

sig sndB : (Beh((a, a))) -> Beh(a)
fun sndB(cB) { fun (t:Float) { snd(cB(t)) } }

sig toPairB : (Beh(a), Beh(a)) -> Beh((a, a))
fun toPairB(xB, yB) { fun (t:Float) { (xB(t), yB(t)) } }

sig toBPair : (Beh((a, a))) -> (Beh(a), Beh(a))
fun toBPair(xB) { (fstB(xB), sndB(xB)) } 

sig const : (a) -> Beh(a)
fun const(v) { fun (t:Float) { v } }

sig iAddB : (Beh(Int), Beh(Int)) -> Beh(Int)
fun iAddB(iB, jB) { fun (t:Float) { iB(t) + jB(t) } }

fun iSubB(iB, jB) { fun (t:Float) { iB(t) - jB(t) } }
fun iMulB(iB, jB) { fun (t:Float) { iB(t) * jB(t) } }
fun iDivB(iB, jB) { fun (t:Float) { iB(t) / jB(t) } }
fun iModB(iB, jB) { fun (t:Float) { mod(iB(t), jB(t)) } }

sig fAddB : (Beh(Float), Beh(Float)) -> Beh(Float)
fun fAddB(iB, jB) { fun (t:Float) { iB(t) +. jB(t) } }

fun fSubB(iB, jB) { fun (t:Float) { iB(t) -. jB(t) } }
fun fMulB(iB, jB) { fun (t:Float) { iB(t) *. jB(t) } }
fun fDivB(iB, jB) { fun (t:Float) { iB(t) /. jB(t) } }

fun fModB(iB, jB) {
    fun (t:Float) {
        var jbt = jB(t);
        var d = iB(t) /. jbt;
        (d -. floor(d)) *. jbt
    }
}

fun itofB(iB) { fun (t:Float) { intToFloat(iB(t)) } }

fun ftoiB(iB) { fun (t:Float) { floatToInt(iB(t)) } }

sig time : () -> Beh(Float)
fun time() { fun (t:Float) { t } }

#sig slowerB : (Beh(Float), Beh(Float)) -> Beh(Float)
sig slowerB : (Beh(a), Beh(Float)) -> Beh(a)
fun slowerB(xB, fB) { 
    fun (t:Float) {
        xB((time() `fDivB` fB)(t))
    } 
}

sig fasterB : (Beh(a), Beh(Float)) -> Beh(a)
fun fasterB(xB, fB) {
    fun (t:Float) {
        xB((time() `fMulB` fB)(t))
    } 
}

sig shapeSlowerB : (SBeh, Beh(Float)) -> SBeh
fun shapeSlowerB(xB, fB) { 
    fun (attr:Attrs) {
        fun (t:Float) {
            xB(attr)((time() `fDivB` fB)(t))
        } 
    }
}

sig shapeFasterB : (SBeh, Beh(Float)) -> SBeh
fun shapeFasterB(xB, fB) { 
    fun (attr:Attrs) {
        fun (t:Float) {
            xB(attr)((time() `fDivB` fB)(t))
        } 
    }
}

sig over : (SBeh, SBeh) -> SBeh
fun over(elm1B, elm2B) {
    fun (attr:Attrs) {
        fun (t:Float) {
            <#>
            {elm2B(attr)(t)}
            {elm1B(attr)(t)}
            </#>
        }
    }
}

#sig move : ((Attrs) -a-> (Float) -a-> b, Beh(Float), Beh(Float)) 
#           -> (Attrs) -> (Float) -a-> b
sig move : (SBeh, Beh(Float), Beh(Float)) -> SBeh
fun move(elmB, xB, yB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with posX = attr.posX `fAddB` xB,
                                 posY = attr.posY `fAddB` yB);

            elmB(new)(t)
        }
    }
}


sig moveA : (SBeh, Beh(FPair)) -> SBeh
fun moveA(elmB, cB:Beh(FPair)) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with posX = attr.posX `fAddB` fstB(cB),
                                 posY = attr.posY `fAddB` sndB(cB));
            elmB(new)(t)
        }
    }
}

fun stretch(elmB, wB, hB) {
    #fun (attr:(width:Beh(Float), height:Beh(Float) |_)) 
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with width = attr.width `fAddB` wB,
                                 height = attr.height `fAddB` hB);
            elmB(new)(t)
        } 
    }
}

sig stretchA : (SBeh, Beh(FPair)) -> SBeh
fun stretchA(elmB, cB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with width = attr.width `fAddB` fstB(cB),
                                 height = attr.height `fAddB` sndB(cB));
            elmB(new)(t)
        } 
    }
}

fun rotateAbout(elmB, aB, coordB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with roAngle = aB, roAbout = coordB))(t)
        } 
    }
}

fun rotate(elmB, aB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with roAngle = aB))(t)
        } 
    }
}

sig withImg : (SBeh, Beh(String)) -> SBeh
fun withImg(elmB, pathB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with hrefImg = pathB))(t)
        }
    }
}

sig withText : (SBeh, Beh(String)) -> SBeh
fun withText(elmB, textB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with text = textB))(t)
        }
    }
}

sig withPoints : (SBeh, Beh(Points)) -> SBeh
fun withPoints(elmB, ptsB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with points = ptsB))(t)
        }
    }
}

sig withColor : (SBeh, Beh(String)) -> SBeh
fun withColor(elmB, colorB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with fill = colorB))(t)
        }
    }
}

sig withStroke : (SBeh, Beh(String)) -> SBeh
fun withStroke(elmB, colorB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with stroke = colorB))(t)
        }
    }
}

#sig polyline : () -> (Attrs) -> (Float) ~> Xml
sig polyline : () -> SBeh
fun polyline() {
    #fun (attr:(points:Beh(Points), 
    #           fill:Beh(String),
    #           stroke:Beh(String), strokeWidth:Beh(Float),
    #           roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) 
    fun (attr:Attrs) {
        fun (t:Float) {
            var f = fun (str:String, (x:Float, y:Float)) {
                        str ^^ intToString(floatToInt(x)) ^^ "," ^^ 
                            intToString(floatToInt(y)) ^^ " "
                    };
            var str = fold_left(f, "", attr.points(t));

            var s = floatToInt(attr.strokeWidth(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <polyline
            transform="rotate({a}, {ri}, {rj})"
            points="{str}" 
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

sig polygon : () -> SBeh
fun polygon() {
    #fun (attr:(points:Beh(Points), 
    #           fill:Beh(String),
    #           stroke:Beh(String), strokeWidth:Beh(Float),
    #           roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) 
    fun (attr:Attrs) {
        fun (t:Float) {
            var f = fun (str:String, (x:Float, y:Float)) {
                        str ^^ intToString(floatToInt(x)) ^^ "," ^^ 
                            intToString(floatToInt(y)) ^^ " "
                    };
            var str = fold_left(f, "", attr.points(t));

            var s = floatToInt(attr.strokeWidth(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <polygon
            transform="rotate({a}, {ri}, {rj})"
            points="{str}" 
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

sig rect : () -> SBeh
fun rect() {
    #fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
    #           height:Beh(Float), fill:Beh(String),
    #           stroke:Beh(String), strokeWidth:Beh(Float),
    #           roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) 
    fun (attr:Attrs) {
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

            <rect 
            transform="rotate({a}, {ri}, {rj})"
            x="{x}" 
            y="{y}"
            width="{intToString(w)}"
            height="{intToString(h)}"
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

sig ellipse : () -> SBeh
fun ellipse() {
#    fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
#               height:Beh(Float), fill:Beh(String),
#               stroke:Beh(String), strokeWidth:Beh(Float),
#               roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) 
    fun (attr:Attrs) {
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

            <ellipse 
            transform="rotate({a}, {ri}, {rj})"
            cx="{intToString(x)}" 
            cy="{intToString(y)}"
            rx="{intToString(w)}"
            ry="{intToString(h)}"
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}


#sig text : () ->
#((posX:Beh(Float), posY:Beh(Float),
#height:Beh(Float), width:Beh(Float),
#fill:Beh(String), hrefImg:Beh (String),
#stroke:Beh(String), strokeWidth:Beh(Float),
#roAbout:Beh((Float, Float)), roAngle:Beh(Float),
#text:Beh(String),
#ffamily:Beh(String), fsize:Beh(Float),
#fweight:Beh(String) |_)) -> (Float) {}~> Xml
sig text : () -> SBeh
fun text() {
#    fun (attr:(posX:Beh(Float), posY:Beh(Float),
#               fill:Beh(String),
#               stroke:Beh(String), strokeWidth:Beh(Float),
#               roAngle:Beh(Float), roAbout:Beh((Float, Float)),
#               text:Beh(String),
#               ffamily:Beh(String), fsize:Beh(Float),
#               fweight:Beh(String) |_)) 
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));

            var s = floatToInt(attr.strokeWidth(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            var fsz = floatToInt(attr.fsize(t));

            <text
            transform="rotate({a}, {ri}, {rj})"
            x="{intToString(x)}" 
            y="{intToString(y)}"
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)};
                   font-family:{attr.ffamily(t)};font-size:{intToString(fsz)};
                   fweight:{attr.fweight(t)}">
            {stringToXml(attr.text(t))}
            </text>
        }
    }
}


sig image : () -> SBeh
fun image() {
#    fun (attr:(posX:Beh(Float), posY:Beh(Float), width:Beh(Float), 
#               height:Beh(Float), hrefImg:Beh(String),
#               roAngle:Beh(Float), roAbout:Beh((Float, Float)) |_)) 
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));
            var w = floatToInt(attr.width(t));
            var h = floatToInt(attr.height(t));

            var a = intToString(floatToInt(attr.roAngle(t)));
            var (i, j) = attr.roAbout(t);
            var ri = intToString(floatToInt(i));
            var rj = intToString(floatToInt(j));

            <image 
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
               height = const(1.0), fill = const("none"), 
               stroke = const("black"), strokeWidth = const(1.0),
               hrefImg = const(""),
               points = const([]),
               roAngle = const(0.0), roAbout = const((0.0, 0.0)),
               text = const(""),
               ffamily = const("Arial"), fsize = const(20.0),
               fweight = const("normal")
               ))(t)}
        </#>
        </svg>
    }
}

# [COMPOSE] ==========================================

# [-1, 1] [1, -1]
var wiggleA = sin;
var waggleA = cos;

# [0, 2] [2, 0]
var pWiggleA = const(1.0) `fAddB` wiggleA;
var pWaggleA = const(1.0) `fAddB` waggleA;


# [FIXME]
fun clocktime() {
    fun (t:Float) {
        var k = intToDate(floatToInt(t));
        #var k = intToDate(serverTime());
        intToString(k.hours) ^^ ":" ^^ intToString(k.minutes) ^^ ":" ^^ 
        intToString(k.seconds) 
    }
}

sig test0 : () -> (String) -> (Float){}->Float
fun test0() {
    fun (a:String) {
        fun (b:Float) {
            b
        }
    }
}
    #var test00 = test0()("hello");

fun compose() {
    #-- luigi shrink & grow
    var w = (const(80.0) `fMulB` pWiggleA) `fAddB` const(80.0);
    var h = (const(60.0) `fMulB` pWiggleA) `fAddB` const(60.0);
    var luigi = const("photos_files/Paperluigi.png");

    #var m1 = stretch(move(image() `withImg` luigi,
    #                        const(400.0), const(100.0)),
    #                 w, h) `shapeSlowerB` const(300.0);
    var m1 = stretch((image() `withImg` luigi) `moveA`
                            toPairB(const(400.0), const(100.0)),
                     w, h) `shapeSlowerB` const(300.0);

    #-- mario revolve
    var x = slowerB((const(200.0) `fMulB` pWiggleA) `fAddB` const(50.0),
                    const(500.0));
    var y = slowerB((const(200.0) `fMulB` pWaggleA) `fAddB` const(50.0),
                    const(500.0));
    var mario = const("photos_files/super_mario_theme.png");

    var m2 = stretch(move(image(), x, y),
                const(100.0), const(100.0)) `withImg` mario;
    
    #-- circle
    var chubby = (const(60.0) `fMulB` wiggleA) `fAddB` const(40.0);
    var chubby2 = chubby `slowerB` const(500.0);
    var d1 = move(ellipse(), const(100.0), const(100.0)); 
    var d2 = stretch(d1, chubby2, chubby2) `withColor` const("red");

    #-- point at the center of mario
    var px = x `fAddB` const(50.0);
    var py = y `fAddB` const(50.0);
    var p1 = stretch(move(ellipse() `withStroke` const("yellow"),
                          px, py),
                     const(3.0), const(3.0)); 

    #-- rectangle
    var r1 = stretch(move(rect(), 
                          px `fAddB` const(50.0), py), 
                     const(20.0), const(20.0));
    #var r1 = stretch(move(rect("r1"), x, y), 

    var r2 = rotateAbout(r1,
                         slowerB(time() `fModB` const(360.0),
                            const(5.0)), 
                         #const((100.0, 300.0)));
                         toPairB(px, py));
                         #toPairB((px, py)));

    #-- text
    var t1 = move(text() `withText` clocktime(), const(400.0),
                const(400.0));
    #-- polyline
    var pts = const([(10.0, 10.0), (10.0, 50.0), (50.0, 50.0), (50.0, 100.0)]);
    var pl = polyline() `withPoints` pts;
    var pg = polygon() `withPoints` pts;
    
    svg("svg1",
        pg `over` t1 `over` p1 `over` d2 `over` r2 `over` m1 `over` m2,
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
