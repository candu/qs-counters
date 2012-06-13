window.addEvent('domready', function() {
    $$('.content-item').addEvent('click', function(event) {
        var counter_id = this.id.substr(8);
        // TODO: this should really be a POST request; need CSRF protection
        new Request.JSON({
            url: '/update/' + counter_id,
            onSuccess: function(data) {
                console.log(JSON.stringify(data));
                if (data.pressed) {
                    this.getChildren('.counter-name').addClass('pressed');
                } else {
                    this.getChildren('.counter-name').removeClass('pressed');
                }
                this.getElements('.count.day').set('text', Math.round(data.day));
                this.getElements('.count.week').set('text', Math.round(data.week));
            }.bind(this)
        }).get();
    });
    $$('.content-item.count').addEvent('mousedown', function(event) {
        this.getChildren('.counter-name').addClass('pressed');
    }).addEvent('mouseup', function(event) {
        this.getChildren('.counter-name').removeClass('pressed');
    });
});
