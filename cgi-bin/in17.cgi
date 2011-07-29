#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

#??
#typename IntB() = ((Int) -> Int);
#typename Behaviour (a) = (Time) -> a;
#typename Attr = [| AInt:(Int) -> Int | AString:(Int) -> String |];
typename Beh(a) = (Float){}~>a;
#typename Beh(a) = forall e::Row. (Float)~e~>a;

var svg_parent_id = "svg0";
var svg_child_id = "svg1";


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

# --------------------------------
#typename Event(a) = (Float){}~>[(Float, a)];
typename Event(a) = Beh([(Float, a)]);

# [HANDLERS] ------------------
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


sig filterE : ((Float, a){}~>Bool, Event(a)) -> Event(a)
fun filterE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((t2, a)) {
                     f(t2, a)
                 };
        filter(f2, evt(t))
    }
}

sig latterE : (Float, Event(a)) -> Event(a)
fun latterE (ms, evt) {
    fun (t:Float) {
        var f2 = fun ((t2, _)) {
                    t2 > t +. ms  
                 };
        filter(f2, evt(t))
    }
}

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

sig snapshot : (Event(a), Beh(b)) ~> Event((a, b)) 
fun snapshot(evt, xB) {
    fun (t:Float) {
        var f = fun ((t2, a)) {
                    (t2, (a, xB(t2)))
                };
        map(f, evt(t))
    }
}

sig snapshot2 : (Event(a), Beh(b)) ~> Event(b) 
fun snapshot2(evt, xB) {
    fun (t:Float) {
        var f = fun ((t2, a)) {
                    (t2, xB(t2))
                };
        map(f, evt(t))
    }
}

fun createE(mgr) (t) {
    spawnWait {
        mgr ! MQuery(t, self());
        var lst = recv ();
        #debug("createE-------" ^^ intToString(length(lst)));
        fun (t2:Float) {
            lst
        }
    }
}

fun mouseClickE(user) {
    var f = fun (t, a) {
                switch(a) {
                    case EClick(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (a) {
                switch(a) {
                    case EMove(x, y) -> (x, y)
                    case EClick(x, y) -> (x, y)
                }
             };

    f2 `mapE` (f `filterE` user)
}
# mmE : Event(User) -> Event(FPair)
fun mouseMoveE(user) {
    var f = fun (t, a) {
                switch(a) {
                    case EMove(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (a) {
                switch(a) {
                    case EMove(x, y) -> (x, y)
                    case EClick(x, y) -> (x, y)
                }
             };

    f2 `mapE` (f `filterE` user)
}

#sig mouseMoveB : (FPair) -> Beh(FPair) 
fun mouseMoveB(mmE) {
    (0.0, 0.0) `stepper` mmE
}

# evts : Event([|EMove:(Float, Float) | EClick:((Float, Float)) |]
# evts : (Float){}~>[(Float, EMove(Float, Float))]
fun createMouseMoveB(evts) {
    var f = fun (t, a) {
                switch(a) {
                    case EMove(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (a) {
                switch(a) {
                    case EMove(x, y) -> (x, y)
                    case EClick(x, y) -> (x, y)
                }
             };
    (0.0, 0.0) `stepper` (f2 `mapE` (f `filterE` evts)) 
}

fun createMouseClickB(evts) {
    var f = fun (t, a) {
                switch(a) {
                    case EClick(_, _) ->
                        true
                    case _ -> false
                }
            };
    var f2 = fun (a) {
                switch(a) {
                    case EMove(x, y) -> (x, y)
                    case EClick(x, y) -> (x, y)
                }
             };
    (0.0, 0.0) `stepper` (f2 `mapE` (f `filterE` evts)) 
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

fun compose(user) {
    var mmE = mouseMoveE(user);
    
    #-- mouse move behaviour
    var mmB = mouseMoveB(mmE);

    #-- circle
    #var d1 = moveA(circleA("d1"), fstB(mmB), sndB(mmB)); 
    var d1 = moveB(circleA("d1"), getCoord(mmB)); 
    var d2 = stretchA(d1, const(50.0), const(50.0));

    svgA(svg_child_id,
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

fun span(f, lst) {
    switch(lst) {
        case [] -> ([], [])
        case (x::xs) ->
            if (f(x)) {
                var (rs, ls) = span(f, xs);
                (x::rs, ls)
            } else {
                ([], lst)
            }
    }
}

fun evtMgr(evts) client {
    receive {
        case MQuery((t, proc)) -> 
            var f = fun ((t2, _)) {
                        t2 < t
                    };
            var (xs, ys) = span(f, evts);
            proc ! xs;
            #
            var f2 = fun ((mm, mc), e) {
                        switch(e) {
                            case (_, EMove(_, _)) ->
                                ([e], mc)
                            case (_, EClick(_, _)) ->
                                (mm, [e])
                        }
                     };
            var (mm, mc) = fold_left(f2, ([], []), xs);
            if (length(mm) == 0 || length(mc) == 0) {
                evtMgr(mm ++ mc ++ ys)
            } else {
                var (mt, _) = hd(mm);
                var (ct, _) = hd(mc);
                if (mt > ct) {
                    evtMgr(mc ++ mm ++ ys)
                } else {
                    evtMgr(mm ++ mc ++ ys)
                }
            }
        case MMove(new) -> # (Float, EMove(Float, Float))
            evtMgr(evts ++ [new])
        case MClick(new) -> # (Float, EClick(Float, Float))
            evtMgr(evts ++ [new])
        #case _ ->
    }
}

fun drawInit2(user, scene, dura) client {
    if (not (pressed("drawImage"))) {
        var now = clientTime();
        var nowf = intToFloat(now);
        #var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))(user(nowf))(nowf);
        var svgXml = scene(user(nowf))(nowf);

        if (isNull(getNodeById(svg_child_id))) {
            appendChildren(svgXml, getNodeById(svg_parent_id));
        } else {
            replaceNode(svgXml, getNodeById(svg_child_id)); 
        };

        draw2(user, scene, now + dura)
    } else {
        removeNode(getNodeById(svg_child_id));
    }
}

fun draw2(user, scene, tEnd) client {
    var now = clientTime();
    if (now <= tEnd) {
        var nowf = intToFloat(now);
        #var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))(user(nowf))(nowf);
        var svgXml = scene(user(nowf))(nowf);
        replaceNode(svgXml, getNodeById(svg_child_id)); 
        draw2(user, scene, tEnd)
    } else { }
}

fun container() {
    var mouseMgr = spawn { evtMgr([]) };
    var user = createE(mouseMgr);
    var scene = compose;

    <#>
    <button id="press1" type="button" 
    l:onclick="{
                   #ignore(spawn { drawInit(scene, 10000) })
                   ignore(spawn { drawInit2(user, scene, 10000) })
               }">draw image1</button>

    <div id="svgbasics" >
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    id="{svg_parent_id}" width="800" height="600"
    viewbox="0 0 800 600" 
    l:onclick="{mouseMgr ! MClick(intToFloat(clientTime()),
                                     EClick(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}"
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
