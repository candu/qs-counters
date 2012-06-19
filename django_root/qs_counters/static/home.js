function elem_to_counter(elem) {
    return parseInt(elem.id.substr(8));
}

function counter_to_elem(counter) {
    return $('counter-' + counter);
}

function init_home_ui(data) {
    $$('.content-item.duration').each(function(elem) {
        var counter = elem_to_counter(elem);
        if (data[counter].pressed) {
            elem.getChildren('.counter-name').addClass('pressed');
            var poll = function() {
                var duration = data[counter].day + (+new Date() / MS_PER_S) - data[counter].last;
                var duration_str = render_duration(duration);
                elem.getElements('.count.day').set('text', duration_str);
            };
            poll();
            window.setInterval(poll, POLL_INTERVAL);
        } else {
          var duration_str = render_duration(data[counter].day);
          elem.getElements('.count.day').set('text', duration_str);
        }
    });
    $$('.content-item.count').each(function(elem) {
        var counter = elem_to_counter(elem);
        elem.getElements('.count.day').set('text', data[counter].day);
    });
    $$('.content-item').addEvent('click', function(event) {
        var counter = elem_to_counter(this);
        window.location.href = '/view/' + counter;
    });
}

window.addEvent('domready', function() {
    new Request.JSON({
        url: '/stats_all',
        onSuccess: init_home_ui
    }).get();
});
