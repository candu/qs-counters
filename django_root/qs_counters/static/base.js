function render_duration(duration) {
    if (duration >= 60 * 60) {
        duration /= 60;
    }
    var hhmm = Math.floor(duration / 60);
    if (hhmm < 10) {
        hhmm = '0' + hhmm;
    }
    var mmss = Math.floor(duration % 60);
    if (mmss < 10) {
        mmss = '0' + mmss;
    }
    return hhmm + ':' + mmss;
}

var MS_PER_S = 1000;
