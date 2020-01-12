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
                success: function () { console.log('post success') }
            });
        }
    }

    // get list of all officers
    const links = $('tbody:last').find('a');

    // for each officer
    for (i = 0; i < links.length; i++) {
        const link = links[i];
        console.log(link.href);

        // make GET request
        link.click();
        await sleep(1000);
        // make GET request to get the officer's info
        $.get("erreport.aspx", function (data) {
            console.log($(data).find("#Label1")[0].innerText);
        });
        await sleep(2000);
        if (i > 5) break;
    }

}, 100);

