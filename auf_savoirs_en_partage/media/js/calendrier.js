function customOpenCalendar(num) {
    var cal_box = document.getElementById(DateTimeShortcuts.calendarDivName1+num)
    var cal_link = document.getElementById(DateTimeShortcuts.calendarLinkName+num)
    var inp = DateTimeShortcuts.calendarInputs[num];

    // With no starting value, try to initialize it with calendar before
    if (!inp.value) {
        var before = num-1;
        if (before >= 0) {
            inp = DateTimeShortcuts.calendarInputs[before];
            DateTimeShortcuts.calendarInputs[num].value = inp.value;
        }
    }

    // Determine if the current value in the input has a valid date.
    // If so, draw the calendar with that date's year and month.
    if (inp.value) {
        var date_parts = inp.value.split('-');
        var year = date_parts[0];
        var month = parseFloat(date_parts[1]);
        if (year.match(/\d\d\d\d/) && month >= 1 && month <= 12) {
    	DateTimeShortcuts.calendars[num].drawDate(month, year);
        }
    }


    // Recalculate the clockbox position
    // is it left-to-right or right-to-left layout ?
    if (getStyle(document.body,'direction')!='rtl') {
        cal_box.style.left = findPosX(cal_link) + 17 + 'px';
    }
    else {
        // since style's width is in em, it'd be tough to calculate
        // px value of it. let's use an estimated px for now
        // TODO: IE returns wrong value for findPosX when in rtl mode
        //       (it returns as it was left aligned), needs to be fixed.
        cal_box.style.left = findPosX(cal_link) - 180 + 'px';
    }
    cal_box.style.top = findPosY(cal_link) - 75 + 'px';

    cal_box.style.display = 'block';
    addEvent(window.document, 'click', function() { DateTimeShortcuts.dismissCalendar(num); return true; });
}

function customAddClock(inp) {
        var num = DateTimeShortcuts.clockInputs.length;
        DateTimeShortcuts.clockInputs[num] = inp;

        // Shortcut links (clock icon and "Now" link)
        var shortcuts_span = document.createElement('span');
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        var now_link = document.createElement('a');
        now_link.setAttribute('href', "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", new Date().getHourMinuteSecond());");
        now_link.appendChild(document.createTextNode(gettext('Now')));
        var clock_link = document.createElement('a');
        clock_link.setAttribute('href', 'javascript:DateTimeShortcuts.openClock(' + num + ');');
        clock_link.id = DateTimeShortcuts.clockLinkName + num;
        quickElement('img', clock_link, '', 'src', DateTimeShortcuts.admin_media_prefix + 'img/admin/icon_clock.gif', 'alt', gettext('Clock'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        shortcuts_span.appendChild(now_link);
        shortcuts_span.appendChild(document.createTextNode('\240|\240'));
        shortcuts_span.appendChild(clock_link);

        // Create clock link div
        //
        // Markup looks like:
        // <div id="clockbox1" class="clockbox module">
        //     <h2>Choose a time</h2>
        //     <ul class="timelist">
        //         <li><a href="#">Now</a></li>
        //         <li><a href="#">Midnight</a></li>
        //         <li><a href="#">6 a.m.</a></li>
        //         <li><a href="#">Noon</a></li>
        //     </ul>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>

        var clock_box = document.createElement('div');
        clock_box.style.display = 'none';
        clock_box.style.position = 'absolute';
        clock_box.className = 'clockbox module';
        clock_box.setAttribute('id', DateTimeShortcuts.clockDivName + num);
        document.body.appendChild(clock_box);
        addEvent(clock_box, 'click', DateTimeShortcuts.cancelEventPropagation);

        quickElement('h2', clock_box, gettext('Choose a time'));
        time_list = quickElement('ul', clock_box, '');
        time_list.className = 'timelist';
        quickElement("a", quickElement("li", time_list, ""), "6:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '06:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "7:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '07:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "8:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '08:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "9:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '09:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "10:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '10:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "11:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '11:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "12:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '12:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "13:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '13:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "14:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '14:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "15:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '15:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "16:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '16:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "17:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '17:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "18:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '18:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "19:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '19:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "20:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '20:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "21:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '21:00:00');")
        quickElement("a", quickElement("li", time_list, ""), "22:00", "href", "javascript:DateTimeShortcuts.handleClockQuicklink(" + num + ", '22:00:00');")

        cancel_p = quickElement('p', clock_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeShortcuts.dismissClock(' + num + ');');
    }

DateTimeShortcuts.addClock = customAddClock;
DateTimeShortcuts.openCalendar = customOpenCalendar;
