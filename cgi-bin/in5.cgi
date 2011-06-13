#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config


# animate can't use xlink
# <animate xlink:href="#c1" ...
# begin="10s" starts from onLoad
fun drawImage1() client { 
    if (not (pressed("drawImage1"))) {
        appendChildren(
            <g xmlns="http://www.w3.org/2000/svg" id="g1" >
            <image xmlns="http://www.w3.org/2000/svg" 
            id="img1" x="250" y="100" width="200" height="150" 
            xlink:href="photos_files/535566372_33c1025c7b_o.jpg"/>
            </g>
            , getNodeById("svg1"));
    } else {
            removeNode(getNodeById("g1"));
    }
}

# 1. stroke-width="7.06" causes error, bcz minus sign '-' 
# 2. <mpath> doesn't work bcz xlink:href doesn't work
fun drawImage2() client { 
    if (not (pressed("drawImage2"))) {
        appendChildren(
            <g xmlns="http://www.w3.org/2000/svg" id="g2" >
            </g>
            , getNodeById("svg1"));

        appendChildren(
            <image xmlns="http://www.w3.org/2000/svg" 
            id="img2" x="450" y="100" width="200" height="150" 
            xlink:href="photos_files/535566372_33c1025c7b_o.jpg"/>
            , getNodeById("g2"));

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
<button id="press1" type="button" l:onclick="{drawImage1()}">
    draw image1</button>
<button id="press2" type="button" l:onclick="{drawImage2()}">
    draw image2</button>

<div id="svgbasics">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" 
id="svg1" width="800px" height="300px" viewbox="0 0 800 300">
            <image xmlns="http://www.w3.org/2000/svg" 
            xmlns:xlink="http://www.w3.org/1999/xlink"
            id="img0" x="50" y="100" width="200" height="150" 
            xlink:href="photos_files/535566372_33c1025c7b_o.jpg"/>
</svg>
</div>
</body>
 </html>
