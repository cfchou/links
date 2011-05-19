#!/Users/cfchou/project/trunk/links --config=/Users/cfchou/Sites/cgi-bin/config

fun drawOnDiv() client { 
    appendChildren(
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" id="svgE">
        </svg>,
        getNodeById("svgbasics"));
    var svg = getNodeById("svgE");

    appendChildren(
        <circle xmlns="http://www.w3.org/2000/svg" cx="100px" cy="100px" r="50px"
        style="fill:red; stroke:black; stroke-width:5" />, svg)
}

page
<html>
<head>
<style>
    #svgbasics {{ width: 300px; height: 300px; border: 1px solid #484; }}
</style>
</head>

<body>
<div id="press">
   <a l:onclick="{drawOnDiv()}">draw</a>
</div>

<div id="svgbasics"></div>
</body>
 </html>
