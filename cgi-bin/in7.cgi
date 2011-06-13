#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

fun drawImage1(t0, t1) client {
    if (not (pressed("drawImage1"))) {
        appendChildren(
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
            id="svg1" width="800px" height="300px" viewbox="0 0 800 300">
                <circle xmlns="http://www.w3.org/2000/svg" 
                id="c1" cx="50" cy="100" r="50"
                style="fill:red; stroke:black; stroke-width:5" />
            </svg>
        , getNodeById("svgbasics"));
        doDrawImage1(t0, t1);
    } else {
            removeNode(getNodeById("svg1"));
    }
}

fun doDrawImage1(t0, nFrame) client {
    var stepT = 100;    # millisecond
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
                    replaceNode(
                        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
                        id="svg1" width="800px" height="300px"
                        viewbox="0 0 800 300">
                            <circle xmlns="http://www.w3.org/2000/svg" 
                            id="c1" cx="{intToString(50 + nFrame * 5)}" 
                            cy="100" r="50"
                            style="fill:red; stroke:black; stroke-width:5" />
                        </svg>
                    , getNodeById("svg1"));
                    doDrawImage1(t0, nFrame + 1);
                } else { }
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
