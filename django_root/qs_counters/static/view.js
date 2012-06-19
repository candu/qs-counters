function init_view_ui(data) {
  console.log(data);
  if (data.type == 'count') {
    $$('.count.day').set('text', data.day);
    $$('.count.week').set('text', data.week);
  } else {
    $$('.count.day').set('text', render_duration(data.day));
    $$('.count.week').set('text', render_duration(data.week));
    if (data.pressed) {
      var poll = function() {
        var duration_day = data.day + (+new Date() / MS_PER_S) - data.last;
        var duration_week = data.week + (+new Date() / MS_PER_S) - data.last;
        var duration_day_str = render_duration(duration_day);
        var duration_week_str = render_duration(duration_week);
        $$('.count.day').set('text', duration_day_str);
        $$('.count.week').set('text', duration_week_str);
      }
      poll();
      window.setInterval(poll, 200);
    }
  }
}

window.addEvent('domready', function() {
  var form = document.forms[0];
  var counter_id = form.counter_id.value;
  new Request.JSON({
    url: '/stats/' + counter_id,
    onSuccess: init_view_ui
  }).get();
});
