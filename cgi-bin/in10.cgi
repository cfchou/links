#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

typename Time = Int;
#??
#typename IntB() = ((Int) -> Int);
#typename Behaviour (a) = (Time) -> a;
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];

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

fun lift0(a) {
    fun(t) {
        a
    }
}

var time = fun (t:Int) { t };

fun addIntB(iB, jB) {
    fun (t:Int) {
        iB(t) + jB(t)
    }
}

fun combineB (elm1B, elm2B) {
    fun (t:Int) {
        <#>
        {elm1B(t)}
        {elm2B(t)}
        </#>
    }
}

fun circle (id) {
    fun (t:Int) {
        <circle xmlns="http://www.w3.org/2000/svg" 
        id="{id}" cx="0" 
        cy="0" r="1"
        style="fill:red; stroke:black; stroke-width:5" />
    }
}

# circle_move(elmB,
#   a.[| CX:(Int) -> Int | CY:(Int) -> Int | R:(Int) -> Int | a|]) 
fun circle_move (elmB, cxB, cyB) {
    fun (t:Int) {
        var xml = elmB(t);
        var name = getAttribute(xml, "id");
        var r = getAttribute(xml, "r");
        <circle xmlns="http://www.w3.org/2000/svg" 
        id="{name}" cx="{intToString(cxB(t))}" 
        cy="{intToString(cyB(t))}" r="{r}"
        style="fill:red; stroke:black; stroke-width:5" />
    }
}

fun circle_offset (elmB, cxB, cyB) {
    fun (t:Int) {
        var xml = elmB(t);
        var name = getAttribute(xml, "id");
        var cx = getAttribute(xml, "cx");
        var cy = getAttribute(xml, "cy");

        circle_move(elmB, addIntB(cxB, lift0(stringToInt(cx))),
            addIntB(cyB, lift0(stringToInt(cy))))
    }
}

fun circle_stretch (elmB, rB) {
    fun (t:Int) {
        var xml = elmB(t);
        var name = getAttribute(elmB(t), "id");
        var cx = getAttribute(xml, "cx");
        var cy = getAttribute(xml, "cy");

        <circle xmlns="http://www.w3.org/2000/svg" 
        id="{name}" cx="{cx}" 
        cy="{cy}" r="{intToString(rB(t))}"
        style="fill:red; stroke:black; stroke-width:5" />
    }
}

fun svg (w, h, elmB) {
    fun (t:Int) {
        var sw = intToString(w);
        var sh = intToString(h);
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
        id="svg1" width="{sw}" height="{sh}"
        viewbox="0 0 {sw} {sh}" >
        <#>
        {elmB(t)}
        </#>
        </svg>
    }
}

fun wiggle (lo:Float, hi:Float) {
    fun (t:Int) {
        var f = intToFloat(t);
        floatToInt((hi -. lo) *. (1.0 +. sin(f)) /. 2.0  +. lo)
    }
}

fun waggle (lo:Float, hi:Float) {
    fun (t:Int) {
        var f = intToFloat(t);
        floatToInt((hi -. lo) *. (1.0 +. cos(f)) /. 2.0  +. lo)
    }
}

# ?? How to/Should I control speed?


# [COMPOSE] =====================================
fun compose() {

    var r = wiggle(20.0, 120.0);
    var x = wiggle(50.0, 500.0);
    var y = waggle(50.0, 500.0);

    #var c1 = circle_stretch(circle_move(circle("c1"), x, lift0(100)), r); 
    var c1 = circle_stretch(circle_move(circle("c2"), x, y), lift0(30)); 
    var c2 = circle_stretch(circle_move(circle("c2"), lift0(500), lift0(150)), r); 
    svg(800, 600, c1 `combineB` c2)
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
