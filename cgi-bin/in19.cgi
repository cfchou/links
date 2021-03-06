#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

typename Time = Float;
typename Beh(a) = (Time){}~>a;

typename FPair = (Float, Float);
typename Points = [FPair];

typename TForm = [|Rotate:Beh((Float, (Float, Float))) | Translate:Beh(FPair) 
                  | Scale:Beh(FPair) | SkewX:Beh(Float) | SkewY:Beh(Float)|];

typename Attrs = (posX:Beh(Float), posY:Beh(Float),
                  height:Beh(Float), width:Beh(Float),
                  fill:Beh(String), hrefImg:Beh (String),
                  stroke:Beh(String), strokeWidth:Beh(Float),
                  transform:[TForm],
                  points:Beh(Points),
                  text:Beh(String),
                  ffamily:Beh(String), fsize:Beh(Float),
                  fweight:Beh(String));

typename SBeh = (Attrs){}~> Beh(Xml);

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

fun fst((a, _)) { a }
fun snd((_, b)) { b }

sig fstB : (Beh((a, b))) -> Beh(a)
fun fstB(cB) { fun (t:Float) { fst(cB(t)) } }

sig sndB : (Beh((a, b))) -> Beh(b)
fun sndB(cB) { fun (t:Float) { snd(cB(t)) } }

sig toPairB : (Beh(a), Beh(b)) -> Beh((a, b))
fun toPairB(xB, yB) { fun (t:Float) { (xB(t), yB(t)) } }

sig toBPair : (Beh((a, b))) -> (Beh(a), Beh(b))
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

sig time : () -> Beh(Float)
fun time() { fun (t:Float) { t } }

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

sig at : (SBeh, Beh(FPair)) -> SBeh
fun at(elmB, cB:Beh(FPair)) {
    fun (attr:Attrs) {
        fun (t:Float) {
            #var new = (attr with posX = attr.posX `fAddB` fstB(cB),
            #                     posY = attr.posY `fAddB` sndB(cB));
            var new = (attr with posX = fstB(cB),
                                 posY = sndB(cB));
            elmB(new)(t)
        }
    }
}

sig sizeof : (SBeh, Beh(FPair)) -> SBeh
fun sizeof(elmB, cB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with width = attr.width `fAddB` fstB(cB),
                                 height = attr.height `fAddB` sndB(cB));
            elmB(new)(t)
        } 
    }
}

sig skewX : (SBeh, Beh(Float)) -> SBeh
fun skewX(elmB, aB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            debug("---------skewX");
            var new = (attr with transform = 
                        SkewX(aB) :: attr.transform);
                        #attr.transform ++ [SkewX(aB)]);
            elmB(new)(t)
        } 
    }
}

sig skewY : (SBeh, Beh(Float)) -> SBeh
fun skewY(elmB, aB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with transform = 
                        attr.transform ++ [SkewY(aB)]);
            elmB(new)(t)
        } 
    }
}

sig scale: (SBeh, Beh(FPair)) -> SBeh
fun scale(elmB, whB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with transform = 
                        attr.transform ++ [Scale(whB)]);
            elmB(new)(t)
        } 
    }
}

sig translate : (SBeh, Beh(FPair)) -> SBeh
fun translate(elmB, atB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            var new = (attr with transform = 
                        attr.transform ++ [Translate(atB)]);
            elmB(new)(t)
        } 
    }
}

sig rotateAbout : (SBeh, Beh(Float), Beh(FPair)) -> SBeh
fun rotateAbout(elmB, aB, whB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            debug("---------rotateAbout");
            var new = (attr with transform = 
                        Rotate(toPairB(aB, whB)) :: attr.transform);
                        #attr.transform ++ [Rotate(toPairB(aB, whB))]);
            elmB(new)(t)
        } 
    }
}

sig rotateA : (SBeh, Beh(Float)) -> SBeh
fun rotateA(elmB, aB) {
    rotateAbout(elmB, aB, const((0.0, 0.0)))
}

sig tformString : (TForm) -> Beh(String)
fun tformString(f) {
    fun (t:Float) {
        switch(f) {
            case Rotate(bh) ->
                var (a, (x, y)) = bh(t);
                "rotate(" ^^ intToString(floatToInt(a)) ^^ ", " ^^
                    intToString(floatToInt(x)) ^^ ", " ^^
                    intToString(floatToInt(y)) ^^ ")"
            case Translate(bh) ->
                var (x, y) = bh(t);
                "translate(" ^^ intToString(floatToInt(x)) ^^ ", " ^^
                    intToString(floatToInt(y)) ^^ ")"
            case Scale(bh) ->
                var (x, y) = bh(t);
                "scale(" ^^ intToString(floatToInt(x)) ^^ ", " ^^
                    intToString(floatToInt(y)) ^^ ")"
            case SkewX(bh) ->
                "skewX(" ^^ intToString(floatToInt(bh(t))) ^^ ")" 
            case SkewY(bh) ->
                "skewY(" ^^ intToString(floatToInt(bh(t))) ^^ ")" 
        }
    }
}

sig multiTFormString : ([TForm]) ~> Beh(String)
fun multiTFormString(fs) {
    var f = fun (a, b) { 
                fun (t:Float) {
                    var str = a(t) ^^ " " ^^ b(t);
                    #debug("---------------" ^^ a(t) ^^ "++" ^^ b(t) ^^ "------------");
                    str
                }
            };
    fold_left(f, const(""), map(tformString, fs))
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

sig polyline : () -> SBeh
fun polyline() {
    fun (attr:Attrs) {
        fun (t:Float) {
            var f = fun (str:String, (x:Float, y:Float)) {
                        str ^^ intToString(floatToInt(x)) ^^ "," ^^ 
                            intToString(floatToInt(y)) ^^ " "
                    };
            var str = fold_left(f, "", attr.points(t));
            var s = floatToInt(attr.strokeWidth(t));

            var trans = multiTFormString(attr.transform)(t);

            <polyline
            transform="{trans}"
            points="{str}" 
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}

sig polygon : () -> SBeh
fun polygon() {
    fun (attr:Attrs) {
        fun (t:Float) {
            var f = fun (str:String, (x:Float, y:Float)) {
                        str ^^ intToString(floatToInt(x)) ^^ "," ^^ 
                            intToString(floatToInt(y)) ^^ " "
                    };
            var str = fold_left(f, "", attr.points(t));
            var s = floatToInt(attr.strokeWidth(t));

            var trans = multiTFormString(attr.transform)(t);

            <polygon
            transform="{trans}"
            points="{str}" 
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}


sig rect : () -> SBeh
fun rect() {
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = intToString(floatToInt(attr.posX(t)));
            var y = intToString(floatToInt(attr.posY(t)));
            var w = floatToInt(attr.width(t));
            var h = floatToInt(attr.height(t));
            var s = floatToInt(attr.strokeWidth(t));

            var trans = multiTFormString(attr.transform)(t);

            <rect 
            transform="{trans}"
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
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));
            var w = floatToInt(attr.width(t) /. 2.0);
            var h = floatToInt(attr.height(t) /. 2.0);
            var s = floatToInt(attr.strokeWidth(t));

            var trans = multiTFormString(attr.transform)(t);

            <ellipse 
            transform="{trans}"
            cx="{intToString(x)}" 
            cy="{intToString(y)}"
            rx="{intToString(w)}"
            ry="{intToString(h)}"
            style="fill:{attr.fill(t)};stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)}" />
        }
    }
}


sig text : () -> SBeh
fun text() {
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));

            var s = floatToInt(attr.strokeWidth(t));
            var fsz = floatToInt(attr.fsize(t));

            var trans = multiTFormString(attr.transform)(t);
            <text
            transform="{trans}"
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
    fun (attr:Attrs) {
        fun (t:Float) {
            var x = floatToInt(attr.posX(t));
            var y = floatToInt(attr.posY(t));
            var w = floatToInt(attr.width(t));
            var h = floatToInt(attr.height(t));

            var trans = multiTFormString(attr.transform)(t);

            <image 
            transform="{trans}"
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
               transform = [],
               text = const(""),
               ffamily = const("Arial"), fsize = const(20.0),
               fweight = const("normal")
               ))(t)}
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

# ------- 
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

#================================

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

#sig mouseMoveE : (Event(a)) -> Event(FPair)
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

# [COMPOSE] ==========================================

# [-1, 1] [1, -1]
var wiggleA = sin;
var waggleA = cos;

# [0, 2] [2, 0]
var pWiggleA = const(1.0) `fAddB` wiggleA;
var pWaggleA = const(1.0) `fAddB` waggleA;


# [FIXME] not accurate
fun clocktime() {
    fun (t:Float) {
        var k = intToDate(floatToInt(t));
        #var k = intToDate(serverTime());
        intToString(k.hours) ^^ ":" ^^ intToString(k.minutes) ^^ ":" ^^ 
        intToString(k.seconds) 
    }
}

# [FIXME] Lazy eval required
fun swapColor(clr1, mE, clr2) {
    var f = fun (clr) {
                if (clr == clr1) {
                    const(clr2)
                } else {
                    const(clr1)
                }
            };
    #sig switcher : (Beh(a), Event(Beh(a))) -> Beh(a)
    #sig mapE : ((a){}~>b, Event(a)) -> Event(b)
    #sig snapshot2 : (Event(a), Beh(b)) ~> Event(b) 
    const(clr1) `switcher` mapE(f, mE `snapshot2` swapColor(clr1, mE, clr2))
}

# [FIXME] call by name required
fun swapColor2(clr1, mE, clr2) {
    var f = fun () {
        switch(getCookie("circlecolor")) {
            case clr1 ->
                setCookie("circlecolor", clr2);
                clr2
            case clr2 ->
                setCookie("circlecolor", clr1);
                clr1
        }
    };
    #sig switcher : (Beh(a), Event(Beh(a))) -> Beh(a)
    #sig mapE : ((a){}~>b, Event(a)) -> Event(b)
    #sig snapshot2 : (Event(a), Beh(b)) ~> Event(b) 
    const(getCookie("circlecolor")) `switcher` (mE `constE` const(f()))
}

fun equalB(aB, bB) {
    fun (t:Float) {
        aB(t) == bB(t)
    }
}

fun suffle(idx) {
    fun (t:Float) {
        var tt = floatToInt(t);
        var d = mod(tt + idx, 4);
        debug("======" ^^ intToString(d) ^^ "-----" ^^ intToString(tt));
        switch (d) {
            case 0 -> "photos_files/IMG_5293.JPG"
            case 1 -> "photos_files/IMG_5299.JPG"
            case 2 -> "photos_files/IMG_5308.JPG"
            case 3 -> "photos_files/IMG_5224.JPG"
        }
    }
}

fun compose(user) {
    var mmE = mouseMoveE(user);
    var mcE = mouseClickE(user);
    #-- mouse move behaviour
    var mmB = mouseMoveB(mmE);

    var img1 = const("photos_files/IMG_5224.JPG")`switcher`
                (mcE `constE` suffle(1)); 
    var img2 = const("photos_files/IMG_5293.JPG")`switcher`
                (mcE `constE` suffle(2)); 
    var img3 = const("photos_files/IMG_5299.JPG")`switcher`
                (mcE `constE` suffle(3)); 
    var img4 = const("photos_files/IMG_5308.JPG")`switcher`
                (mcE `constE` suffle(4)); 
    var photo1 = image() `withImg` img1 `at` const((50.0, 50.0))
                    `sizeof` const((80.0, 60.0));
    var photo2 = image() `withImg` img2 `at` const((150.0, 50.0))
                    `sizeof` const((80.0, 60.0));
    var photo3 = image() `withImg` img3 `at` const((50.0, 150.0))
                    `sizeof` const((80.0, 60.0));
    var photo4 = image() `withImg` img4 `at` const((150.0, 150.0))
                    `sizeof` const((80.0, 60.0));

    var cclr = const("red") `switcher` (mcE `constE` const("blue"));

    #var cclr2 = swapColor2("red", mcE, "green");

    #-- luigi shrink & grow
    var w = (const(80.0) `fMulB` pWiggleA) `fAddB` const(80.0);
    var h = (const(60.0) `fMulB` pWiggleA) `fAddB` const(60.0);
    var luigi = const("photos_files/Paperluigi.png");

    var m1 = image() `withImg` luigi 
                `at` toPairB(const(400.0), const(300.0)) 
                `sizeof` toPairB(w, h) 
                `shapeSlowerB` const(300.0);
    var m3 = m1 `at` const((400.0, 100.0));

    #-- mario revolve
    var x = slowerB((const(200.0) `fMulB` pWiggleA) `fAddB` const(50.0),
                    const(500.0));
    var y = slowerB((const(200.0) `fMulB` pWaggleA) `fAddB` const(50.0),
                    const(500.0));
    var mario = const("photos_files/super_mario_theme.png");

     var m2 = image() `at` toPairB(x, y)
                 `sizeof` toPairB(const(100.0), const(100.0))
                 `withImg` mario;
    
    #-- circle
    var chubby = (const(60.0) `fMulB` wiggleA) `fAddB` const(40.0);
    var chubby2 = chubby `slowerB` const(500.0);
    #var d1 = ellipse() `at` toPairB(const(100.0), const(100.0)); 
    var d1 = ellipse() `at` mmB;
    #var d2 = d1 `sizeof` toPairB(chubby2, chubby2) `withColor` const("red");
    var d2 = d1 `sizeof` toPairB(chubby2, chubby2) `withColor` cclr;

    #-- point at the center of mario
    var px = x `fAddB` const(50.0);
    var py = y `fAddB` const(50.0);
    var p1 = ellipse() `withStroke` const("yellow") 
                `at` toPairB(px, py)
                `sizeof` toPairB(const(3.0), const(3.0)); 

    #-- rectangle
    var r1 = rect() `at` toPairB(px `fAddB` const(50.0), py) 
              `sizeof` toPairB(const(20.0), const(20.0));

    var r2 = rotateAbout(r1,
                         slowerB(time() `fModB` const(360.0),
                            const(5.0)), 
                         toPairB(px, py));
    var r3 = r2 `skewX` const(45.0);

    #-- text
    var t1 = text() `withText` clocktime() `at` 
                toPairB(const(400.0), const(400.0));
    #-- polyline
    var pts = const([(10.0, 10.0), (10.0, 50.0), (50.0, 50.0), (50.0, 100.0)]);
    var pl = polyline() `withPoints` pts;
    var pg = polygon() `withPoints` pts;
    
    svg("svg1",
        #pg `over` t1 `over` p1 `over` d2 `over` r3 `over` m3 `over` m2,
        photo1 `over` photo2 `over` photo3 `over` photo4,
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
            var f = fun ((t2, _)) {
                        t2 < t
                    };
            var (xs, ys) = span(f, evts);
            proc ! xs;

            # discard all event before t, except for the last MMove
            var f2 = fun (mm, e) {
                        switch(e) {
                            case (_, EMove(_, _)) -> [e]
                            case _ -> mm
                        }
                     };
            var mm = fold_left(f2, [], xs);
            evtMgr(mm ++ ys)

        case MMove(new) -> # (Float, EMove(Float, Float))
            evtMgr(evts ++ [new])
        case MClick(new) -> # (Float, EClick(Float, Float))
            evtMgr(evts ++ [new])
        #case _ ->
    }
}

fun drawInit(user, scene, dura) client {
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

        draw(user, scene, now + dura)
    } else {
        removeNode(getNodeById(svg_child_id));
    }
}

fun draw(user, scene, tEnd) client {
    var now = clientTime();
    if (now <= tEnd) {
        var nowf = intToFloat(now);
        #var svgXml = (scene : ((Float)~?~>Xml) <- Beh(Xml))(user(nowf))(nowf);
        var svgXml = scene(user(nowf))(nowf);
        replaceNode(svgXml, getNodeById(svg_child_id)); 
        draw(user, scene, tEnd)
    } else { }
}


fun container() {
    var mouseMgr = spawn { evtMgr([]) };
    var user = createE(mouseMgr);
    var scene = compose;

    <#>
    <button id="press1" type="button" 
    l:onclick="{
                   ignore(spawn { drawInit(user, scene, 10000) })
               }">draw image1</button>

    <div id="svgbasics" >
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    id="{svg_parent_id}" width="800" height="600"
    viewbox="0 0 800 600" 
    l:onclick="{var t = clientTime();
                debug("= = = = = =" ^^ intToString(t));
                mouseMgr ! MClick(intToFloat(t),
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
