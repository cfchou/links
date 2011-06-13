#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


# animate can't use xlink
# <animate xlink:href="#c1" ...
fun drawAnimate() client { 
    if (not (pressed("drawAnimate"))) {
        appendChildren(
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            id="svg1" width="300px" height="300px" viewbox="0 0 300 300">
            <circle xmlns="http://www.w3.org/2000/svg" 
            id="c1" cx="60" cy="100" r="50"
            style="fill:red; stroke:black; stroke-width:5" >
                <animate xmlns="http://www.w3.org/2000/svg"  
                attributeName="cx" 
                begin="click" dur="5s" from="60" to="200" /> 
            </circle>
            </svg>,
            getNodeById("svgbasics"));
    } else {
            removeNode(getNodeById("svg1"));
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
    #svgbasics {{ width: 300px; height: 300px; border: 1px solid #484; }}
</style>
</head>

<body>
<button id="press1" type="button" l:onclick="{drawAnimate()}">draw animate</button>
<div id="svgbasics">
</div>
</body>
 </html>
