/** Scrape data on officers from the Executive Record Sheets of Indian Forest
 * Service (IFS). The database link is at http://ifs.nic.in/ExRecSheet.aspx
 *
 * Usage:
 * 1. From the above link, pick a Cadre (region) and enter the required captcha.
 * 2. Select "Detailed Report" to get to a list of all officials.
 * 3. Run the below JavaScript in the browser (copy all, paste, and enter in the
 * browser developer console) to download all that juicy data. */


/* Inject jQuery into the page */
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js');
document.head.appendChild(jQueryScript);

window.$ = $;

setTimeout(() => {  // wait for scripts to load

    // get list of all officers
    const links = $('tbody:last').find('a');

    // for each officer
    for (i = 2; i < links.length; i++) {
        const link = links[i];
        // extract __EVENTTARGET parameter from link
        let __EVENTTARGET = link.href.match(/__doPostBack\('(.*)',''/)[1];

        // convert __EVENTTARGET paramerer to an HTML-formatted string
        __EVENTTARGET = encodeURIComponent(__EVENTTARGET);
        console.log(__EVENTTARGET);

        // make POST request to set the active officer
        $.post("reportersheet.aspx", { __EVENTTARGET: __EVENTTARGET, __EVENTARGUMENT: '' }, () => {
            setTimeout(() => {
                // make GET request to get the officer's info
                $.get("erreport.aspx", function (data) {
                    console.log($(data).find("#Label1")[0].innerText);
                });
            }, 1000);

        });
        if (i > 4) break;
    }

}, 100);

