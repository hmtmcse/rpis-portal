PWeb.scanner = (function () {

    function onScanSuccess(decodedText, decodedResult) {
        PWeb.ajax.call({
            method: "GET",
            dataType: "html",
            url: PWeb.baseURL + "/volunteer/scan-details?id=" + decodedText,
            success: function (content) {
                let place = jQuery("#details-table")
                place.html("")
                place.html(content)
            }
        })
    }

    return {
        rescan: function () {
            jQuery(document).on("click", ".btn-success", function () {
                let _this = jQuery(this)
                let id = _this.attr("data-id")
                let key = _this.attr("data-key")
                let qt = _this.attr("data-qt")
                PWeb.ajax.call({
                    method: "GET",
                    dataType: "html",
                    url: PWeb.baseURL + "/volunteer/update-scan-item?id=" + id + "&key=" + key + "&quantity=" + qt,
                    success: function (content) {
                        let place = _this.closest(".my-td")
                        place.html("")
                        place.html(content)
                    }
                })
            })
        },
        initScanner: function (domId = "reader") {
            let config = {
                fps: 10,
                qrbox: 250,
                rememberLastUsedCamera: true,
                supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
            };
            let html5QrcodeScanner = new Html5QrcodeScanner(
                domId, config
            );
            html5QrcodeScanner.render(onScanSuccess);
        }
    }

}());

jQuery(document).ready(function () {
    PWeb.scanner.initScanner()
    PWeb.scanner.rescan()
});