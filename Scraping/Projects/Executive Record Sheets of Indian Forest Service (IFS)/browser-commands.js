/** Scrape data on officers from the Executive Record Sheets of Indian Forest
 * Service (IFS). The database link is at http://ifs.nic.in/ExRecSheet.aspx
 *
 * Usage:
 * 1. From the above link, pick a Cadre (region) and enter the required captcha.
 * 2. Select "Detailed Report" to get to a list of all officials.
 * 3. Run the below JavaScript in the browser (copy all, paste, and enter in the
 * browser developer console) to download all that juicy data. */

// function to sleep for a certain amount of time
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
    // override form behaviour to submit without redirect
    __doPostBack = function (eventTarget, eventArgument) {
        if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
            theForm.__EVENTTARGET.value = eventTarget;
            theForm.__EVENTARGUMENT.value = eventArgument;
            // theForm.submit();
            $.ajax({
                url: 'reportersheet.aspx',
                type: 'post',
                data: $('#form1').serialize(),
                success: function () {
                    // console.log(`post success (${getElapsedTimeSinceLastMeasure()} ms)`);
                }
            });
        }
    }

    // get list of all officers
    const links = $('tbody:last').find('a');

    // for each officer
    for (i = 0; i < links.length; i++) {
        const link = links[i];

        // make GET request
        link.click();
        await sleep(5000); // ~3000ms per POST request
        // make GET request to get the officer's info
        getElapsedTimeSinceLastMeasure()
        $.get("erreport.aspx", function (data) {
            const officerName = $(data).find("#Label1")[0].innerText;
            // console.log(`GET success (${getElapsedTimeSinceLastMeasure()} ms)`);
            console.log(officerName);
        });
        await sleep(1500);  // ~350 ms per GET request
        if (i > 5) break;
    }

}, 100);

