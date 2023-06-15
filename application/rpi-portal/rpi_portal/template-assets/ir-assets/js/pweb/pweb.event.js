PWeb.event = (function () {
    return {
        totalParticipantSelect: function (selector, params) {
            jQuery(document).on("change", selector, function () {
                let _this = jQuery(this)
                let total = _this.val()
                PWeb.ajax.call({
                    method: "GET",
                    dataType: "html",
                    url: PWeb.baseURL + "/event-booking-manage?" + params + "=" + total,
                    success: function (content) {
                        let place = jQuery("#table-wrapper")
                        place.html("")
                        place.html(content)
                    }
                })
            })
        },
        initSelect: function () {
            PWeb.event.totalParticipantSelect("#total-adult-select", "adult")
            PWeb.event.totalParticipantSelect("#total-child-select", "child")
        }
    }
}());

jQuery(document).ready(function () {
    PWeb.event.initSelect()
});
