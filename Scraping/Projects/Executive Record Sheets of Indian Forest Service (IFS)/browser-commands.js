/** Scrape data on officers from the Executive Record Sheets of Indian Forest
 * Service (IFS). The database link is at http://ifs.nic.in/ExRecSheet.aspx
 *
 * Usage:
 * 1. From the above link, pick a Cadre (region) and enter the required captcha.
 * 2. Select "Detailed Report" to get to a list of all officials.
 * 3. Run the below JavaScript in the browser (copy all, paste, and enter in the
 * browser developer console) to download all that juicy data. */

/* download a string to a local file */
function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/* Inject jQuery into the page */
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js');
document.head.appendChild(jQueryScript);

window.$ = $;

var lastTime = new Date().getTime();

function getElapsedTimeSinceLastMeasure() {
    const newTime = new Date().getTime();
    const diff = newTime - lastTime;
    lastTime = newTime;
    return diff;
}

setTimeout(async () => {  // wait for scripts to load
    jQuery.ajaxSetup({ async: false });

    // override form behaviour to submit without redirect
    __doPostBack = async function (eventTarget, eventArgument) {
        if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
            theForm.__EVENTTARGET.value = eventTarget;
            theForm.__EVENTARGUMENT.value = eventArgument;
            // theForm.submit();
            await $.ajax({
                url: 'reportersheet.aspx',
                type: 'post',
                data: $('#form1').serialize(),
                success: function () { },
                async: false
            });
        }
    }

    // get list of all officers
    const links = $('tbody:last').find('a');

    // for each officer
    for (i = 0; i < links.length; i++) {
        const link = links[i];

        getElapsedTimeSinceLastMeasure()
        // make GET request
        link.click();
        await sleep(4)
        // make GET request to get the officer's info
        await $.ajax({
            url: 'erreport.aspx',
            type: 'get',
            success: function (data) {
                const officerName = $(data).find("#Label1")[0].innerText;
                const elapsedTime = getElapsedTimeSinceLastMeasure();
                download(data, `IFS-HTML ${i + 1} ${officerName}.html`, 'text/html');
                console.log(`${officerName} (${elapsedTime} ms) ${i}/${links.length}=${i / links.length}`);
            },
            async: false
        });
    }

}, 100);

