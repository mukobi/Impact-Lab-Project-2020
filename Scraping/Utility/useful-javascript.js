
/* download a JSON object to a local file
    @param content: JSON content
    @param fileName: *.json or other text file
    @param contentType: "application/json" or other file type */
function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([JSON.stringify(content)], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
download(jsonData, 'data.json', 'application/json'); // usage


/* Inject jQuery into the document */
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js');
document.head.appendChild(jQueryScript);

/* jQuery Post */
$.post("url", { data: null }, function (result) {
    console.log(result);
});