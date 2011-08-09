#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

typename Time = Float;
typename Beh(a) = (Time){}~>a;

typename FPair = (Float, Float);
typename Points = [FPair];

typename TForm = [|Rotate:Beh((Float, FPair)) | Translate:Beh(FPair) 
                  | Scale:Beh(FPair) | SkewX:Beh(Float) | SkewY:Beh(Float)|];

typename FontWeight = [|Normal:() | Bold:()|];
typename FontStyle = [|Normal:() | Italic:()|];

typename Attrs = (posX:Beh(Float), posY:Beh(Float),
                  height:Beh(Float), width:Beh(Float),
                  fill:Beh(String), hrefImg:Beh (String),
                  stroke:Beh(String), strokeWidth:Beh(Float),
                  transform:[TForm],
                  points:Beh(Points),
                  text:Beh(String),
                  ffamily:Beh(String), fsize:Beh(Float),
                  fweight:Beh(FontWeight), fstyle:Beh(FontStyle));

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

fun itosB(iB) { fun (t:Float) { intToString(iB(t)) } }
fun ftosB(iB) { fun (t:Float) { floatToString(iB(t)) } }

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
            debug("---------translate");
            var new = (attr with transform = 
                        attr.transform ++ [Translate(atB)]);
                        #Translate(atB)::attr.transform);
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
                        #Rotate(toPairB(aB, whB)) :: attr.transform);
                        attr.transform ++ [Rotate(toPairB(aB, whB))]);
            elmB(new)(t)
        } 
    }
}

sig rotate : (SBeh, Beh(Float)) -> SBeh
fun rotate(elmB, aB) {
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
                    debug("---------------" ^^ a(t) ^^ "++" ^^ b(t) ^^ "------------");
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

sig withText : (SBeh, Beh(String)) -> SBeh
fun withText(elmB, textB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with text = textB))(t)
        }
    }
}

sig withFontFamily : (SBeh, Beh(String)) -> SBeh
fun withFontFamily(elmB, ffB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with ffamily = ffB))(t)
        }
    }
}

sig withFontSize : (SBeh, Beh(Float)) -> SBeh
fun withFontSize(elmB, fszB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with fsize = fszB))(t)
        }
    }
}

sig withFontWeight : (SBeh, Beh(FontWeight)) -> SBeh
fun withFontWeight(elmB, fwB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with fweight = fwB))(t)
        }
    }
}

sig withFontStyle : (SBeh, Beh(FontStyle)) -> SBeh
fun withFontStyle(elmB, fsB) {
    fun (attr:Attrs) {
        fun (t:Float) {
            elmB((attr with fstyle = fsB))(t)
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

fun fweightToString(fw:FontWeight) {
    switch (fw) {
        case Normal -> "normal"
        case Bold -> "bold"
    }
}

fun fstyleToString(fw:FontStyle) {
    switch (fw) {
        case Normal -> "normal"
        case Italic -> "italic"
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
            var fw = fweightToString(attr.fweight(t));
            var fs = fstyleToString(attr.fstyle(t));

            debug(">>>>> text");
            var trans = multiTFormString(attr.transform)(t);
            debug("<<<<< text");
            <text
            transform="{trans}"
            x="{intToString(x)}" 
            y="{intToString(y)}"
            style="fill:{attr.fill(t)};
                   stroke:{attr.stroke(t)};
                   stroke-width:{intToString(s)};
                   font-family:{attr.ffamily(t)};
                   font-size:{intToString(fsz)};
                   font-weight:{fw};
                   font-style:{fs}" >
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
               fweight = const(Normal), fstyle = const(Normal)))(t)}
        </#>
        </svg>
    }
}

# [LAZY LIST]--------------------------------
typename LLst(a) = mu x . ((){}~>[|Nil|Cons:(a,x)|]);

sig lhd: (LLst(a)) {}~> a
fun lhd(llst) {
    switch (llst()) {
        case Nil -> error("lhd: empty list")
        case Cons(x, _) -> x
    }
}

sig ltl: (LLst(a)) {}~> LLst(a)
fun ltl(llst) {
    switch (llst()) {
        case Nil -> error("ltl: empty list")
        case Cons(_, lxs) -> lxs
    }
}

sig llen: (LLst(a)) {}~> Int
fun llen(llst) {
    fun llen_ (llst, n) {
        switch (llst()) {
            case Nil -> n
            case Cons(_, lxs) -> llen_(lxs, n + 1)
        }
    }
    llen_(llst, 0)
}

sig lmap: ((a) {}~> b, LLst(a)) {}~> LLst(b)
fun lmap(f, llst) () {
   switch(llst()) {
       case Nil -> Nil
       case Cons(x, lxs) -> Cons(f(x), lmap(f, lxs))
    }
}

sig lfilter: ((a) {}~> Bool, LLst(a)) {}~> LLst(a)
fun lfilter(f, llst) () {
    switch (llst()) {
        case Nil -> Nil
        case Cons(x, lxs) ->
            if (f(x)) {
                Cons(x, lfilter(f, lxs))
            } else {
                lfilter(f, lxs)()
            }
    }
}

sig lselect: (LLst(a), Int) {}~> a
fun lselect(llst, n) {
    if (n == 0) {
        lhd(llst)
    } else {
        lselect(ltl(llst), n - 1)
    }
}

sig ltakeWhile: ((a) {}~> Bool, LLst(a)) {}~> LLst(a)
fun ltakeWhile(f, llst) () {
    switch (llst()) {
        case Nil -> Nil
        case Cons(x, lxs) ->
            if (f(x)) {
                Cons(x, ltakeWhile(f, lxs))
            } else {
                Nil
            }
    }
}

#sig ldropWhile: ((a) {}~> Bool, LLst(a)) {}~> LLst(a)
fun ldropWhile(f, llst) () {
    switch (llst()) {
        case Nil -> Nil
        case Cons(x, lxs) ->
            if (f(x)) {
                ldropWhile(f, lxs)()
            } else {
                Cons(x, lxs)
            }
    }
}

sig lfoldl: ((b, a) {}~> b, b, LLst(a)) ~> b
fun lfoldl(f, b, llst) {
    switch (llst()) {
        case Nil -> b
        case Cons(x, lxs) -> lfoldl(f, f(b, x), lxs)
    }
}

sig lfoldr: ((a, b) {}~> b, b, LLst(a)) ~> b
fun lfoldr(f, b, llst) {
    switch (llst()) {
        case Nil -> b
        case Cons(x, lxs) -> f(x, lfoldr(f, b, lxs))
    }
}

sig lappend: (LLst(a), LLst(a)) {}~> LLst(a)
fun lappend(llst1, llst2) () {
    switch(llst1()) {
        case Nil -> llst2()
        case Cons(x, lxs) -> Cons(x, lappend(lxs, llst2))
    }
}

sig lreverse: (LLst(a)) {}~> LLst(a)
fun lreverse(llst) {
    fun f(lxs, x) () {
        Cons(x, lxs)
    }
    lfoldl(f, fun() { Nil }, llst)
}

sig lzip: (LLst(a), LLst(a)) {}~> LLst((a, a))
fun lzip(llst1, llst2) () {
    switch (llst1()) {
        case Nil -> Nil
        case Cons(x, lxs) -> 
            switch (llst2()) {
                case Nil -> Nil
                case Cons(y, lys) -> 
                    Cons((x, y), lzip(lxs, lys))
            }
    }
}

sig lunzip: (LLst((a, b))) {}~> (LLst(a), LLst(b))
fun lunzip(llst) {
    switch(llst()) {
        case Nil -> (fun () { Nil }, fun () { Nil })
        case Cons((a, b), lxs) ->
            var (las, lbs) = lunzip(lxs);
            (fun () { Cons(a, las) }, fun () { Cons(b, lbs) })
    }
}

# --------------------------------
typename LEvent(a) = Beh(LLst((Float, a)));

# [HANDLERS] ------------------
# +=>
sig handleLE : ((Float, a){}~>b, LEvent(a)) -> LEvent(b)
fun handleLE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((te, a)) {
                     (te, f(te, a))
                 };
        lmap(f2, evt(t))
    }
}

# ==>
sig mapLE : ((a){}~>b, LEvent(a)) -> LEvent(b)
fun mapLE(f, evt) {
    var f2 = fun (_, a) {
                 f(a)
             };
    handleLE(f2, evt)
}

#-=>
sig constLE : (LEvent(a), b) -> LEvent(b)
fun constLE(evt, b) {
    var f = fun (_, _) { b };
    handleLE(f, evt)
}

sig filterLE : ((Float, a){}~>Bool, LEvent(a)) -> LEvent(a)
fun filterLE(f, evt) {
    fun (t:Float) {
        var f2 = fun ((te, a)) {
                     f(te, a)
                 };
        lfilter(f2, evt(t))
    }
}

# ------- 
sig lswitcher : (Beh(a), LEvent(Beh(a))) -> Beh(a)
fun lswitcher(b, evt) {
    fun (t:Float) {
        #fun g ((_, e)) { e }
        #var (_, lst) = lunzip(ldropWhile(f, evt(t)));
        #var lst = lmap(g, ldropWhile(f, evt(t)));

        # either b or last behaviour in the event stream
        switch (evt(t)()) {
            case Nil -> 
                debug("------------------ Nil");
                b(t)
            case Cons((_, x), _) ->
                debug("++++++++++++++++++ not Nil");
                x(t)
        }
    }
}

sig lstepper : (a, LEvent(a)) -> Beh(a)
fun lstepper(a, evt) {
    lswitcher(const(a), mapLE(const, evt))
}


# --------------------------------
# mouse click event constructor
# mouseClickLE : (LEvent ([|EClick:(a, b)|EDown:(a, b)|EMove:(a, b)|EUp:(a, b)|])) -> LEvent ((a, b))
fun mouseClickLE(user) {
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
                    case EDown(x, y) -> (x, y)
                    case EUp(x, y) -> (x, y)
                }
             };

    f2 `mapLE` (f `filterLE` user)
}

#sig mouseMoveLE : (Event(a)) -> Event(FPair)
fun mouseMoveLE(user) {
    var f = fun (_, a) {
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
                    case EDown(x, y) -> (x, y)
                    case EUp(x, y) -> (x, y)
                }
             };

    f2 `mapLE` (f `filterLE` user)
}


#\t -> [(td, ((xd, yd), (\t -> [(tu, (xu, yu))])))]
#fun mouseDownLE(user) {

fun mouseMoveLB(mmE) {
    (0.0, 0.0) `lstepper` mmE
}

# --------------------------------
#typename Event(a) = (Float){}~>[(Float, a)];
#typename Event(a) = Beh([(Float, a)]);

#================================
# universal event constructor
# createE: (Process ({ hear:[|MQuery:(a, Process ({ hear:b|_ }))|_|]|_ })) 
#           -> (a) ~> (Float) -> b
fun createE(mgr) (t:Float) {
    spawnWait {
        mgr ! MQuery(t, self());
        var lst = recv ();
        fun (t2:Float) {
            lst
        }
    }
}


# [COMPOSE] ==========================================

# [-1, 1] [1, -1]
var wiggle = sin;
var waggle = cos;

# [0, 2] [2, 0]
var pWiggle = const(1.0) `fAddB` wiggle;
var pWaggle = const(1.0) `fAddB` waggle;

fun pointAdd(aB, bB) {
    toPairB(fstB(aB) `fAddB` fstB(bB), sndB(aB) `fAddB` sndB(bB))
}

fun compose(user) {
    var mmE = mouseMoveLE(user);
    #var mdE = mouseDownLE(user);
    var mcE = mouseClickLE(user);
    #-- mouse move behaviour
    var mmB = mouseMoveLB(mmE);
    
    # temporarily move
    #var dragMmB = clickFlipB(mdE, const((80.0, 60.0)), mmB);

    # permenantly move
    #var afterMUp = fun ((x, y)) { const((x, y)) };
    #var dragMmB2 = clickMapB(mdE, const((280.0, 60.0)), mmB, afterMUp);

    #var img2 = clickFlipB(mdE, const("photos_files/IMG_5224.JPG"), 
    #    const("photos_files/IMG_5293.JPG")); 
    var c1 = ellipse() `at` mmB 
                       `sizeof` const((50.0, 50.0))
                       `withColor` const("red");


    svg("svg1",
        c1,
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

fun evtMgr(evts:LLst(?)) client {
    receive {
        case MQuery((t, proc)) -> 
              var f = fun ((t2, _)) {
                          t2 > t
                      };
              var xs = ldropWhile(f, evts);
              proc ! xs;
              evtMgr(evts)
        case MMove(new) -> # (Float, EMove(Float, Float))
            var xs = fun () {
                        Cons(new, evts)
                        #Nil
                     };
            evtMgr(xs)
            #evtMgr(evts)
        case MClick(new) -> # (Float, EClick(Float, Float))
            evtMgr(fun() { Cons(new, evts) })
            #evtMgr(evts)
        case MDown(new) -> # (Float, EDown(Float, Float))
            evtMgr(fun() { Cons(new, evts) })
            #evtMgr(evts)
        case MUp(new) -> # (Float, EUp(Float, Float))
            evtMgr(fun() { Cons(new, evts) })
            #evtMgr(evts)
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
    var mouseMgr = spawn { evtMgr(fun () { Nil }) };
    var user = createE(mouseMgr);

    <#>
    <button id="press1" type="button" 
    l:onclick="{
                   ignore(spawn { drawInit(user, compose, 30000) })
               }">draw image1</button>

    <div id="svgbasics" >
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
    xmlns:xlink="http://www.w3.org/1999/xlink"
    width="800" height="600"
    viewbox="0 0 800 600" 
    l:onmousedown="{var t = getTime(event);
                debug("= = = = = =" ^^ intToString(t));
                mouseMgr ! MDown(intToFloat(t),
                                     EDown(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}"
    l:onmouseup="{var t = getTime(event);
                debug("= = = = = =" ^^ intToString(t));
                mouseMgr ! MUp(intToFloat(t),
                                     EUp(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}"
    l:onclick="{var t = getTime(event);
                debug("= = = = = =" ^^ intToString(t));
                mouseMgr ! MClick(intToFloat(t),
                                     EClick(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}" 
    l:onmousemove="{mouseMgr ! MMove(intToFloat(getTime(event)),
                                     EMove(intToFloat(getPageX(event)),
                                            intToFloat(getPageY(event))))}" > 

    <line x1="0" y1="0" x2="300" y2="0" style="stroke:red;stroke-width:5" />
    <line x1="0" y1="0" x2="0" y2="200" style="stroke:red ;stroke-width:5" />

    <g id="{svg_parent_id}">

    <line x1="0" y1="0" x2="300" y2="0" style="stroke:green;stroke-width:5" />
    <line x1="0" y1="0" x2="0" y2="200" style="stroke:green ;stroke-width:5" />

    </g>
    </svg>
    </div>
    </#>
}

    #<g id="{svg_parent_id}" transform="translate(-10,-35)">
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
