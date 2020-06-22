function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
    xmlHttp.onload = function()
    {
        if (xmlHttp.status == 200)
        {
            document.getElementById("main_div").innerHTML = xmlHttp.response;
        }
    }
    xmlHttp.send();
}