#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


# animate can't use xlink
# <animate xlink:href="#c1" ...
# begin="10s" starts from onLoad
fun drawAnimate() client { 
    if (not (pressed("drawAnimate"))) {
        appendChildren(
            <g xmlns="http://www.w3.org/2000/svg" id="g1" >
            <circle xmlns="http://www.w3.org/2000/svg" 
            id="c1" cx="50" cy="50" r="30"
            style="fill:red; stroke:black; stroke-width:3" >
                <animate xmlns="http://www.w3.org/2000/svg"  
                attributeName="cx" 
                begin="10s" dur="5s" from="50" to="200" /> 
            </circle>
            </g>
            , getNodeById("svg1"));
    } else {
            removeNode(getNodeById("g1"));
    }
}

# 1. stroke-width="7.06" causes error, bcz minus sign '-' 
# 2. <mpath> doesn't work bcz xlink:href doesn't work
fun drawAnimateMotion() client { 
    if (not (pressed("drawAnimateMotion"))) {
        appendChildren(
            <g xmlns="http://www.w3.org/2000/svg" id="g2" >
            <path xmlns="http://www.w3.org/2000/svg" 
            id="path1" d="M100,250 C 100,50 400,50 400,250"
            style="fill:none; stroke:blue; stroke-width:3" />

            <circle xmlns="http://www.w3.org/2000/svg" 
            id="c2" cx="50" cy="100" r="30"
            style="fill:yellow; stroke:black; stroke-width:3" >
                <animateMotion xmlns="http://www.w3.org/2000/svg" 
                path="M100,250 C 100,50 400,50 400,250"
                repeatCount="indefinite" dur="5s" rotate="auto" >
                </animateMotion>
            </circle>
            </g>
            , getNodeById("svg1"));
    } else {
            removeNode(getNodeById("g2"));
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
<button id="press1" type="button" l:onclick="{drawAnimate()}">
    draw animate</button>
<button id="press2" type="button" l:onclick="{drawAnimateMotion()}">
    draw animateMotion</button>

<div id="svgbasics">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
id="svg1" width="800px" height="300px" viewbox="0 0 800 300">
</svg>
</div>
</body>
 </html>
