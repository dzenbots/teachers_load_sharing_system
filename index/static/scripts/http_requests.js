function httpGet(theUrl, div_id)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
    xmlHttp.onload = function()
    {
        if (xmlHttp.status == 200)
        {
            document.getElementById(div_id).innerHTML = xmlHttp.response;
        }
    }
    xmlHttp.send();
}


function httpPost(theUrl, formObj){
    var formData = new FormData(formObj)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", theUrl, true ); // false for synchronous request
    xmlHttp.onload = function()
    {
        if (xmlHttp.status == 200)
        {
            alert("Данные сохранены")
        }
    }
    xmlHttp.send(formData);
}