#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

#??
#typename IntB() = ((Int) -> Int);
#typename Behaviour (a) = (Time) -> a;
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];
typename Beh(a) = (Float){}~>a;
#typename Beh(a) = forall e::Row. (Float)~e~>a;


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

fun moveA(elmB, xB, yB) {
    fun (xB2, yB2, wB, hB) {
        fun (t:Float) {
            elmB(xB `fAddB` xB2,
                 yB `fAddB` yB2,
                 wB, hB)(t)
        }
    }
}

fun stretchA(elmB, wB2, hB2) {
    fun (xB, yB, wB, hB) {
        fun (t:Float) {
            elmB(xB, yB,
                 wB `fMulB` wB2,
                 hB `fMulB` hB2)(t)
        } 
    }
}

fun combineA(elm1B, elm2B) {
    fun (xB, yB, wB, hB) {
        fun (t:Float) {
            <#>
            {elm1B(xB, yB, wB, hB)(t)}
            {elm2B(xB, yB, wB, hB)(t)}
            </#>
        }
    }
}

fun circleA(id) {
    fun (xB, yB, wB, hB) {
        fun (t:Float) {
            var x = floatToInt(xB(t));
            var y = floatToInt(yB(t));
            var h = floatToInt(hB(t) /. 2.0);
            var w = floatToInt(wB(t) /. 2.0);
            if (w == h) {
                <circle id="{id}" 
                cx="{intToString(x)}" 
                cy="{intToString(y)}"
                r="{intToString(w)}"
                style="fill:red; stroke:black; stroke-width:5" />
            } else {
                <ellipse id="{id}"  
                cx="{intToString(x)}" 
                cy="{intToString(y)}"
                rx="{intToString(w)}"
                ry="{intToString(h)}"
                style="fill:red; stroke:black; stroke-width:5" />
            }
        }
    }
}

fun imageA(id, path) {
    fun (xB, yB, wB, hB) {
        fun (t:Float) {
            var x = floatToInt(xB(t));
            var y = floatToInt(yB(t));
            var h = floatToInt(hB(t));
            var w = floatToInt(wB(t));

            <image id="{id}" 
            x="{intToString(x)}" 
            y="{intToString(y)}" 
            width="{intToString(w)}" 
            height="{intToString(h)}" 
            xlink:href="{path}"/>
        }
    }
}

fun svgA (id, elmB, wB, hB) {
    fun (t:Float) {
        var sw = intToString(floatToInt(wB(t)));
        var sh = intToString(floatToInt(hB(t)));
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
        xmlns:xlink="http://www.w3.org/1999/xlink"
        id="{id}" width="{sw}" height="{sh}"
        viewbox="0 0 {sw} {sh}" >

        <#>
        {elmB(const(0.0), const(0.0), const(1.0), const(1.0))(t)}
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
    var w = (const(60.0) `fMulB` pWiggleA);
    var h = (const(45.0) `fMulB` pWiggleA);

    var m1 = stretchA(moveA(imageA("m1", "photos_files/Paperluigi.png"),
                const(500.0), const(75.0)),
                slowerB(const(300.0), w),
                slowerB(const(300.0), h));

    #-- image2 revolve
    var x = (const(100.0) `fMulB` pWiggleA);
    var y = (const(100.0) `fMulB` pWaggleA);

    var m2 = stretchA(moveA(imageA("m2",
                "photos_files/super_mario_theme.png"),
                slowerB(const(1500.0), x),
                slowerB(const(500.0), y)),
                const(60.0), const(45.0));
    
    #-- circle
    var chubby = (const(60.0) `fMulB` wiggleA) `fAddB` const(40.0);
    var chubby2 = slowerB(const(500.0), chubby);
    var d1 = moveA(circleA("d1"), const(100.0), const(100.0)); 
    var d2 = stretchA(d1, chubby2, chubby2);

    svgA("svg1",
        d2 `combineA` m1 `combineA` m2,
        const(800.0), const(600.0))
}


# [WEB] ==========================================
fun drawImage(mouseMgr, scene, t0, tEnd) client {
    if (not (pressed("drawImage"))) {

        var svgXml = scene(intToFloat(clientTime()));
        appendChildren(svgXml, getNodeById("svgbasics"));
        doDrawImage(scene, t0, tEnd);

    } else {
        mouseMgr ! Stop;
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

# ====================

#sig drawing : (?, forall e::Row. (Float) ~e~> Xml, ?, ?) {:[|Latest:Int|j|]|k}~> ?
sig drawing : (?, Beh(Xml), ?, ?) {:[|Latest:Int|j|]|k}~> ?
fun drawing(mouseMgr, scene, t0, tEnd) client {
    receive {
        case Latest(t) -> {
            var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))(intToFloat(t));
            appendChildren(svgXml, getNodeById("svgbasics"));
            drawing(mouseMgr, scene, t0, tEnd)
            #doDrawImage(scene, t0, tEnd)
        }
        case _ -> 
            drawing(mouseMgr, scene, t0, tEnd)
    }
}

fun updating(proc, lst) client {
       receive {
           case MouseMove(t, (x, y)) ->
                #error("MouseMove");
                updating(proc, (t, Move(x, y))::lst) 
           case MouseClick(t, (x, y)) ->
                #error("MouseClick");
                updating(proc, (t, Click(x, y))::lst)
#           case Lookup(t) ->
#                #error(intToString(t));
#                proc ! lst;
#                updating(proc, lst)
           case Stop ->
                waiting([])
           case _ ->
                updating(proc, lst)
       }
}

fun waiting(lst) client {
       receive {
           case Update(t, proc) ->
                #error(intToString(t) ^^ ":" ^^ intToString(x) ^^ 
                #      ":" ^^ intToString(y));
                proc ! Latest(t);
                updating(proc, (t, Start)::[])
            #case Lookup(_, _) ->
            case _ -> waiting([])
       }
}

var scene = compose();

fun container() client {
    var mouseMgr = spawn { waiting([]) };
    <#>
    <button id="press1" type="button" 
    l:onclick="{
                   var t = clientTime(); 
                   var proc = spawn { 
                       drawing(mouseMgr, scene, t, t + 10000)};
                   mouseMgr ! Update(t, proc);
               }">draw image1</button>

    <div id="svgbasics" >
    </div>
    <div id="touchpad"
    l:onmousemove="{mouseMgr ! MouseMove(clientTime(), (getPageX(event),
                                   getPageY(event)))}"
    l:onclick="{mouseMgr ! MouseClick(clientTime(), (getPageX(event),
                                   getPageY(event)))}" >
    </div>
    </#>
}

page
<html>
<head>
<style>
    #svgbasics {{ width: 800px; height: 300px; border: 1px solid #484; }}
    #touchpad {{ width: 800px; height: 200px; border: 2px solid #484; }}
</style>
</head>

<body>
{ container() }
</body>
 </html>
