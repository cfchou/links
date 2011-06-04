#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


fun drawOnDiv() client { 
    if (not (pressed())) {
        appendChildren(
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" id="svg1">
            <circle xmlns="http://www.w3.org/2000/svg" cx="100px" cy="100px" r="50px"
            style="fill:red; stroke:black; stroke-width:5" />
            </svg>,
            getNodeById("svgbasics"));
    } else {
            removeNode(getNodeById("svg1"));
    }
}

fun pressed() client {
    if ("pressed" == getCookie("pressed101")) {
        setCookie("pressed101", "");
        true
    } else {
        setCookie("pressed101", "pressed");
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
<button id="press" type="button" l:onclick="{drawOnDiv()}">draw</button>

<div id="svgbasics"></div>
</body>
 </html>
