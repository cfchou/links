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

fun fst((a, _)) { a }
fun snd((_, b)) { b }

sig const : (a)->Beh(a)
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

fun moveB(elmB, posB) {
    fun (xB2, yB2, wB, hB) {
        fun (t:Float) {
            var (x, y) = posB(t);
            elmB(const(x) `fAddB` xB2,
                 const(y) `fAddB` yB2,
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

fun toCoord(xB, yB) {
    fun (t:Float) {
        (xB(t), yB(t))
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

# [VList] ==========================================
typename VList(a) = mu x.[|Nil|Cons:(a,x)|];

#unzip : ([(a, b)]) ~> ([a], [b])
sig vUnzip : (VList((a, b))) ~> (VList(a), VList(b))
fun vUnzip(vs) {
    switch(vs) {
        case Nil -> (Nil, Nil)
        case Cons((a, b), xs) ->
            var (ms, ns) = vUnzip(xs);
            (Cons(a, ms), Cons(b, ns))
    }
}

#takeWhile : ((a) ~b~> Bool, [a]) ~b~> [a]
sig vTakeWhile : ((a) ~b~> Bool, VList(a)) ~b~> VList(a)
fun vTakeWhile(f, vs) {
    switch(vs) {
        case Nil -> Nil
        case Cons(a, xs) ->
            if (f(a)) {
               Cons(a, vTakeWhile(f, xs)) 
            } else {
                vTakeWhile(f, xs)
            }
    }
}

#length : ([_]) -> Int
fun vLengthH(vs, n) {
    switch(vs) {
        case Nil -> n
        case Cons(_, xs) ->
            vLengthH(xs, n + 1)
    }
}

sig vLength : (VList(_)) ~> Int
fun vLength(vs) {
    vLengthH(vs, 0)
}


fun vReverseH (vs, result) {
    switch(vs) {
        case Nil -> result
        case Cons(a, xs) -> vReverseH(xs, Cons(a, result))
    }
}

#reverse : ([a]) ~> [a]
sig vReverse : (VList(a)) ~> VList(a)
fun vReverse (vs) {
    vReverseH(vs, Nil)
}


#hd : ([a]) ~> a
sig vHd : (VList(a)) ~> a
fun vHd(vs) {
    switch(vs) {
        case Cons(a, _) -> a
        case Nil -> error("vHd: access violation")
    }
}

#tl : ([a]) ~> [a]
sig vTl : (VList(a)) ~> VList(a)
fun vTl(vs) {
    switch(vs) {
        case Cons(_, xs) -> xs
        case Nil -> error("vTl: access violation")
    }
}

#select : ([a], Int) ~> a
sig vSelect : (VList(a), Int) ~> a
fun vSelect(vs, n) {
    if (n == 0) {
        vHd(vs)
    } else {
        vSelect(vTl(vs), n - 1)
    }
}

#map : ((a) -b-> c, [a]) -b-> [c]
sig vMap : ((a) ~b~> c, VList(a)) ~b~> VList(c)
fun vMap(f, vs) {
    switch(vs) {
        case Nil -> Nil
        case Cons(a, xs) ->
            Cons(f(a), vMap(f, xs))
    }
}

#filter : ((a) -b-> Bool, [a]) -b-> [a]
sig vFilter : ((a) ~b~> Bool, VList(a)) ~b~> VList(a)
fun vFilter(f, vs) {
    switch(vs) {
        case Nil -> Nil
        case Cons(a, xs) ->
            if (f(a)) {
                Cons(a, vFilter(f, xs))
            } else {
                vFilter(f, xs)
            }
    }
}

sig vAppend : (VList(a), VList(a)) ~> VList(a)
fun vAppend(vs1, vs2) {
    switch(vs1) {
        case Cons(a, Nil) -> Cons(a, vs2)
        case Cons(a, xs) -> Cons(a, vAppend(xs, vs2))
        case Nil -> vs2
    }
}

# [VEVENT] ==========================================
typename VEvent(a) = (Float){}~>VList((Float, a));

sig vSwitcher : (Beh(a), VEvent(Beh(a))) -> Beh(a)
fun vSwitcher(b, evt) {
    fun (t:Float) {
        var (_, lst) = vUnzip(vTakeWhile(fun ((t2, _)) { t2 < t }, evt(t)));
        var lst2 = Cons(b, lst);
        # either b or last behaviour in the event stream
        vSelect(lst2, vLength(lst2) - 1)(t)
    }
}

sig vStepper : (a, VEvent(a)) -> Beh(a)
fun vStepper(a, evt) {
    vSwitcher(const(a), vMapE(const, evt))
}

# ==>
sig vMapE : ((a){}~>b, VEvent(a)) -> VEvent(b)
fun vMapE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((t, a)) {
                     (t, f(a))
                 };
        vMap(f2, evt(t))
    }
}

#
sig vFilterE : ((Float, a){}~>Bool, VEvent(a)) -> VEvent(a)
fun vFilterE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((t, a)) {
                     f(t, a)
                 };
        vFilter(f2, evt(t))
    }
}

fun vCreateMouseMoveB(mouseE) {
    var f = fun (t, a) {
                switch(a) {
                    case EMove(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (EMove(x, y)) {
                    (x, y)
             };
    (0.0, 0.0) `vStepper` (f2 `vMapE` (f `vFilterE` mouseE)) 
}


# [EVENT] ==========================================
typename Event(a) = (Float){}~>[(Float, a)];

sig switcher : (Beh(a), Event(Beh(a))) -> Beh(a)
fun switcher(b, evt) {
    fun (t:Float) {
        var (_, lst) = unzip(takeWhile(fun ((t2, _)) { t2 < t }, evt(t)));
        var lst2 = b::lst;
        # either b or last behaviour in the event stream
        select(lst2, length(lst2) - 1)(t)
    }
}

sig stepper : (a, Event(a)) -> Beh(a)
fun stepper(a, evt) {
    switcher(const(a), mapE(const, evt))
}

# mosueE : Event([|EMove:(Float, Float) | EClick:((Float, Float)) |]
# mouseE : (Float){}~>[(Float, EMove(Float, Float))]
fun createMouseMoveB(mouseE) {
    var f = fun (t, a) {
                switch(a) {
                    case EMove(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (EMove(x, y)) {
                    (x, y)
             };
    (0.0, 0.0) `stepper` (f2 `mapE` (f `filterE` mouseE)) 
}

fun testE(mouseE) {
    var get = fun ((t, _)) {
                  t 
              };
    fun (t:Float) {
        var lst = mouseE(t);
        var sz = length(lst);
        if (sz > 3) {
            var a = get(select(lst, 0));
            var b = get(select(lst, 0));
            var c = get(select(lst, 0));
            debug(floatToString(a) ^^ ":debug"
                  ^^ floatToString(a) ^^ ":" 
                  ^^ floatToString(a));
            (300.0, 100.0)
        } else {
            debug("testE--------------------------");
            (100.0, 100.0)
        }
    }
}


# +=>
sig handleE : (Event(a), (Float, a){}~>b) -> Event(b)
fun handleE(evt, f) {
    fun (t:Float) {
        var f2 = fun ((a, b)) {
                     (a, f(a, b))
                 };
        map(f2, evt(t))
    }
}

# ==>
sig mapE : ((a){}~>b, Event(a)) -> Event(b)
fun mapE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((t, a)) {
                     (t, f(a))
                 };
        map(f2, evt(t))
    }
}

#-=>
sig constE : (Event(a), b) -> Event(b)
fun constE(evt, b) {
    var f = fun (_) { b };
    f `mapE` evt 
}

#
sig filterE : ((Float, a){}~>Bool, Event(a)) -> Event(a)
fun filterE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((t, a)) {
                     f(t, a)
                 };
        filter(f2, evt(t))
    }
}


# [COMPOSE] ========================================

var wiggleA = sin;
var waggleA = cos;

var pWiggleA = const(1.0) `fAddB` wiggleA;
var pWaggleA = const(1.0) `fAddB` waggleA;

fun fstB(cB) {
    fun (t:Float) {
        var (x, _) = cB(t);        
        x
    }
}

fun sndB(cB) {
    fun (t:Float) {
        var (_, y) = cB(t);        
        y
    }
}

fun getCoord(cB) {
    fun (t:Float) {
        var (x, y) = cB(t);
        (x, y)
    }
}

fun compose(mouseE) {
    #-- mouse move behaviour
    var mmB = vCreateMouseMoveB(mouseE);
    #var mmB = createMouseMoveB(mouseE);
    #var coord = getCoord(mmB);

    #var mmB = testE(mouseE);
    #

    #-- circle
    #var d1 = moveA(circleA("d1"), fstB(mmB), sndB(mmB)); 
    var d1 = moveB(circleA("d1"), getCoord(mmB)); 
    var d2 = stretchA(d1, const(50.0), const(50.0));

    svgA("svg1",
        d2,
        const(800.0), const(600.0))
}


# [WEB] ==========================================

fun pressed(s) client {
    if (s == getCookie(s)) {
        setCookie(s, "");
        true
    } else {
        setCookie(s, s);
        false
    }
}

fun evtMgr(evts) client {
    receive {
        case MQuery((t, proc)) -> 
            var lst = vTakeWhile((fun ((t2, _)) {
                                    t2 < t 
                                 }), evts);
            proc ! lst;
            evtMgr(evts)
        case MMove(new) -> # (Float, EMove(Float, Float))
            #debug("mmove:---------------" ^^ intToString(n));
            evtMgr(evts `vAppend` Cons(new, Nil))
        case _ ->
    }
}

fun evtMgr2(evts) client {
    receive {
        case MQuery((t, proc)) -> 
            var rev = vReverse(evts);
            var lst = vTakeWhile((fun ((t2, _)) {
                                    t2 < t 
                                 }), rev);
            proc ! lst;
            evtMgr(evts)
        case MMove(new) -> # (Float, EMove(Float, Float))
            #debug("mmove:---------------" ^^ intToString(n));
            evtMgr(Cons(new, evts))
        case _ ->
    }
}

fun createMouseE(mgr) (t) {
    spawnWait {
        mgr ! MQuery(t, self());
        recv ()
    }
}

fun drawInit(svg, scene, dura) client {
    if (not (pressed("drawImage"))) {
        var now = clientTime();
        var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))(intToFloat(now));
        appendChildren(svgXml, getNodeById("svg0"));
        draw(scene, now + dura)
    } else {
        removeNode(getNodeById("svg1"));
    }
}

fun draw(scene, tEnd) client {
    var now = clientTime();
    if (now <= tEnd) {
        var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))
                        (intToFloat(now));
        var name = getAttribute(svgXml, "id");
        replaceNode(svgXml, getNodeById(name)); 
        #replaceNode(<g id="gid">{svgXml}</g>, getNodeById("gid")); 
        draw(scene, tEnd)
    } else { }
}

fun container() {
    #var mouseMgr = spawn { evtMgr([]) };
    var mouseMgr = spawn { evtMgr(Nil) };
    var mouseE = createMouseE(mouseMgr);
    var scene = compose(mouseE);
    <#>
    <button id="press1" type="button" 
    l:onclick="{
                   ignore(spawn { drawInit("svg0", scene, 10000) })
               }">draw image1</button>
    <div id="svgbasics" >
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    id="svg0" width="800" height="600"
    viewbox="0 0 800 600" 
    l:onmousemove="{mouseMgr ! MMove(intToFloat(clientTime()),
                                     EMove(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}" />
    </div>
    </#>
}

# =====================================================

page
<html>
<head>
<style>
    #svgbasics {{ width: 800px; height: 600px; border: 1px solid #484; }}
</style>
</head>

<body>
{ container() }
</body>
 </html>
