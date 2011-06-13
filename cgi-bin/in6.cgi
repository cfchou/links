#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

# begin="10s" starts from onLoad
# can't <set attributeName="xlink:href" ... />
fun drawImage1() client { 
    if (not (pressed("drawImage1"))) {
        #var now = intToString(clientTime()) ^^ "s";

        appendChildren(
            <g xmlns="http://www.w3.org/2000/svg" id="g1" >
            <image xmlns="http://www.w3.org/2000/svg" 
            id="img1" x="10" y="10" width="200" height="150" 
            xlink:href="photos_files/535566372_33c1025c7b_o.jpg" >
                <set xmlns="http://www.w3.org/2000/svg"  
                attributeName="xlink:href" 
                begin="5s"
                to="photos_files/313940834_8bf97d364e_b.jpg" />

                <animateTransform xmlns="http://www.w3.org/2000/svg"  
                attributeName="transform" 
                type="rotate" additive="sum" 
                begin="click"
                from="0" to="45" dur="5s" />
            </image>
            <animate xmlns="http://www.w3.org/2000/svg"  
            xlink:href="#img1"
            attributeName="x" 
            begin="click" dur="5s" from="10" to="400" /> 
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
            id="img2" x="10" y="150" width="200" height="150" 
            xlink:href="photos_files/535566372_33c1025c7b_o.jpg"/>
            , getNodeById("g2"));

        appendChildren(
            <path xmlns="http://www.w3.org/2000/svg" 
            id="path2" 
            d="M 100 200 C 200 100 300 0 400 100 C 500 200 600 300 700 200" 
            fill="none" stroke="red"></path>  
            , getNodeById("g2"));

        appendChildren(
            <animateMotion xmlns="http://www.w3.org/2000/svg" 
            id="am2"
            xlink:href="#img2"
            repeatCount="indefinite" dur="5s" rotate="auto" >
            <mpath xlink:href="#path2" />
            </animateMotion>
            , getNodeById("svg1"));
    } else {
            removeNode(getNodeById("am2"));
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
</svg>
</div>
</body>
 </html>
