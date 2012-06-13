window.addEvent('domready', function() {
    $$('.content-item').addEvent('click', function(event) {
        var counter_id = this.id.substr(8);
        // TODO: this should really be a POST request; need CSRF protection
        new Request.JSON({
            url: '/update/' + counter_id,
            onSuccess: function(data) {
                console.log(JSON.stringify(data));
                if (data.pressed) {
                    this.addClass('pressed');
                } else {
                    this.removeClass('pressed');
                }
            }.bind(this)
        }).get();
    });
    $$('.content-item.count').addEvent('mousedown', function(event) {
        this.addClass('pressed');
    }).addEvent('mouseup', function(event) {
        this.removeClass('pressed');
    });
});
