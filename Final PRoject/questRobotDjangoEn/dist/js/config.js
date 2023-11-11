/**
 * api url
 * @type {string}
 */
const BASE_URL = 'http://' + window.location.host

function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function now_time() {

    var nowdate = new Date();

    var year = nowdate.getFullYear(),

        month = nowdate.getMonth() + 1,

        date = nowdate.getDate(),

        h = nowdate.getHours(),

        m = nowdate.getMinutes(),

        s = nowdate.getSeconds(),

        h = checkTime(h),

        m = checkTime(m),

        s = checkTime(s);

    return year + "/" + month + "/" + date + " " + h + ":" + m + ":" + s;
}