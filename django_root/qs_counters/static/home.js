function elem_to_counter(elem) {
    return parseInt(elem.id.substr(8));
}

function counter_to_elem(counter) {
    return $('counter-' + counter);
}

window._counter_intervals = {};

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

function init_counter_ui(data) {
    $$('.content-item.duration').each(function(elem) {
        var counter = elem_to_counter(elem);
        var duration_str = render_duration(data[counter].day);
        elem.getElements('.count.day').set('text', duration_str);
    }).addEvent('click', function(event) {
        var counter_name = this.getChildren('.counter-name')[0];
        counter_name.toggleClass('pressed');
        var counter = elem_to_counter(this);
        this.getElements('.count.day').set('text', 'loading...');
        new Request.JSON({
            url: '/update/' + counter,
            onSuccess: function(data) {
                if (counter_name.hasClass('pressed')) {
                    var MS_PER_S = 1000;
                    var start = +new Date() - Math.floor(data.day * MS_PER_S);
                    window._counter_intervals[counter] = window.setInterval(function() {
                        var duration = (+new Date() - start) / MS_PER_S;
                        var duration_str = render_duration(duration);
                        this.getElements('.count.day').set('text', duration_str);
                    }.bind(this), 200);
                } else {
                    window.clearInterval(window._counter_intervals[counter]);
                    window._counter_intervals[counter] = null;
                    var duration_str = render_duration(data.day);
                    this.getElements('.count.day').set('text', duration_str);
                }
            }.bind(this)
        }).get();
    });
    $$('.content-item.count').each(function(elem) {
        var counter = elem_to_counter(elem);
        elem.getElements('.count.day').set('text', data[counter].day);
    }).addEvent('mousedown', function(event) {
        this.getChildren('.counter-name').addClass('pressed');
    }).addEvent('mouseup', function(event) {
        this.getChildren('.counter-name').removeClass('pressed');
    }).addEvent('click', function(event) {
        var counter = elem_to_counter(this);
        this.getElements('.count.day').set('text', 'loading...');
        new Request.JSON({
            url: '/update/' + counter,
            onSuccess: function(data) {
                this.getElements('.count.day').set('text', Math.round(data.day));
            }.bind(this)
        }).get();
    });
}

window.addEvent('domready', function() {
    new Request.JSON({
        url: '/stats_all',
        onSuccess: init_counter_ui
    }).get();
});
